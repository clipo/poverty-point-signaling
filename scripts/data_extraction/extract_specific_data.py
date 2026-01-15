#!/usr/bin/env python3
"""
Targeted Data Extraction for Poverty Point Project

Extracts specific data types needed for model calibration:
1. Radiocarbon dates with proper parsing (BP dates, calibrated ranges)
2. Construction volumes (especially mound volumes in cubic meters)
3. Exotic goods quantities and sources
4. Site hierarchy data

This is a more targeted version than extract_pdf_data.py, with
improved patterns and data cleaning.

Usage:
    python extract_specific_data.py                    # Process priority PDFs
    python extract_specific_data.py --all              # Process all PDFs
    python extract_specific_data.py --dates            # Only extract dates
    python extract_specific_data.py --volumes          # Only extract volumes
"""

import argparse
import csv
import re
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

try:
    import pymupdf as fitz
except ImportError:
    import fitz

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
PDF_DIR = PROJECT_ROOT / "pdfs"
OUTPUT_DIR = PROJECT_ROOT / "data" / "extracted"

# Priority PDFs for data extraction (per plan.md)
PRIORITY_PDFS = {
    "dates": [
        "Kidder - 2002*",
        "Kidder - 2006*",
        "*Ortmann*",
        "Webb-1956*",
    ],
    "volumes": [
        "*Ortmann*",
        "Kidder - 2002*",
        "Ford - 1954*",
    ],
    "exotic": [
        "DirectionalExchange*",
        "Hays-2018*",
        "Webb-1956*",
        "Webb - 1968*",
    ],
}


@dataclass
class C14Date:
    """Parsed radiocarbon date."""
    source: str
    page: int
    lab_number: str
    date_bp: int
    error: int
    cal_start_bc: Optional[int] = None
    cal_end_bc: Optional[int] = None
    material: str = ""
    site: str = ""
    feature: str = ""
    raw_text: str = ""


@dataclass
class ConstructionVolume:
    """Mound/earthwork volume measurement."""
    source: str
    page: int
    feature: str
    volume_m3: float
    original_value: str
    original_unit: str
    notes: str = ""
    raw_text: str = ""


@dataclass
class ExoticMaterial:
    """Exotic material with source info."""
    source: str
    page: int
    material: str
    quantity: str = ""
    source_region: str = ""
    distance_km: str = ""
    artifact_type: str = ""
    site: str = ""
    raw_text: str = ""


class TargetedExtractor:
    """Extract specific data types from PDFs."""

    # Improved regex patterns
    PATTERNS = {
        # Radiocarbon: "3530 ± 70 BP" or "3530±70 B.P."
        'c14_full': re.compile(
            r'(\d{3,5})\s*[±+\-]\s*(\d{2,4})\s*(?:years?\s*)?(?:B\.?P\.?|bp)',
            re.IGNORECASE
        ),
        # Lab numbers
        'lab_num': re.compile(
            r'\b((?:Beta|GX|M|SI|Tx|UGa|ISGS|AA|CAMS|OxA|Wk|ETH|UCIAMS|OS|I)-?\d{3,6})\b',
            re.IGNORECASE
        ),
        # Calibrated ranges: "1800-1400 cal BC" or "cal. 1800-1400 B.C."
        'cal_bc': re.compile(
            r'(?:cal(?:ibrated)?\.?\s*)?(\d{3,4})\s*[-–—to]+\s*(\d{3,4})\s*(?:cal\.?\s*)?(?:B\.?C\.?(?:E\.?)?|BCE)',
            re.IGNORECASE
        ),
        # Calibrated BP
        'cal_bp': re.compile(
            r'(?:cal(?:ibrated)?\.?\s*)?(\d{3,5})\s*[-–—to]+\s*(\d{3,5})\s*(?:cal\.?\s*)?(?:B\.?P\.?)',
            re.IGNORECASE
        ),

        # Volume in cubic meters: "750,000 m³" or "750000 cubic meters"
        'vol_m3': re.compile(
            r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:cubic\s*)?(?:m(?:eters?)?[³3]|m3|cu\.?\s*m)',
            re.IGNORECASE
        ),
        # Volume in cubic yards
        'vol_yd3': re.compile(
            r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:cubic\s*)?(?:y(?:ar)?ds?[³3]|yd3|cu\.?\s*y)',
            re.IGNORECASE
        ),
        # Volume in cubic feet
        'vol_ft3': re.compile(
            r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:cubic\s*)?(?:f(?:ee)?t[³3]|ft3|cu\.?\s*f)',
            re.IGNORECASE
        ),

        # Mound names
        'mound': re.compile(
            r'\b(Mound\s*[A-F]|Bird\s*Mound|Motley\s*Mound|Lower\s*Jackson\s*Mound|Dunbar\s*Mound)\b',
            re.IGNORECASE
        ),
        # Ridge references
        'ridge': re.compile(
            r'\b(Ridge\s*\d|(?:inner|outer)\s+ridge(?:s)?)\b',
            re.IGNORECASE
        ),

        # Exotic materials with quantities
        'copper_qty': re.compile(
            r'(\d+)\s*(?:pieces?|specimens?|items?|fragments?|objects?)?\s*(?:of\s+)?(?:native\s+)?copper',
            re.IGNORECASE
        ),
        'steatite_qty': re.compile(
            r'(\d+)\s*(?:pieces?|specimens?|items?|fragments?|objects?)?\s*(?:of\s+)?(?:steatite|soapstone)',
            re.IGNORECASE
        ),
        'galena_qty': re.compile(
            r'(\d+)\s*(?:pieces?|specimens?|items?|fragments?|objects?)?\s*(?:of\s+)?galena',
            re.IGNORECASE
        ),

        # Source regions for exotics
        'great_lakes': re.compile(r'Great\s+Lakes?|Lake\s+Superior|Upper\s+Michigan', re.IGNORECASE),
        'appalachian': re.compile(r'Appalachian|Blue\s+Ridge|Piedmont|Georgia|Alabama', re.IGNORECASE),
        'ozark': re.compile(r'Ozark|Missouri|Arkansas\s+(?:River|Valley)', re.IGNORECASE),

        # Site trinomials
        'site_num': re.compile(r'\b(16[A-Z]{2}\d{1,4}|22[A-Z]{2}\d{1,4})\b'),
    }

    # Unit conversion factors to cubic meters
    UNIT_CONVERSIONS = {
        'm³': 1.0,
        'm3': 1.0,
        'yd³': 0.764555,  # cubic yards to cubic meters
        'yd3': 0.764555,
        'ft³': 0.0283168,  # cubic feet to cubic meters
        'ft3': 0.0283168,
    }

    def __init__(self):
        self.dates: list[C14Date] = []
        self.volumes: list[ConstructionVolume] = []
        self.exotics: list[ExoticMaterial] = []
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def get_context(self, text: str, start: int, end: int, chars: int = 200) -> str:
        """Extract surrounding context."""
        ctx_start = max(0, start - chars)
        ctx_end = min(len(text), end + chars)
        return ' '.join(text[ctx_start:ctx_end].split())

    def extract_page_text(self, pdf_path: Path, page_num: int) -> str:
        """Extract text from single page."""
        doc = fitz.open(str(pdf_path))
        try:
            if page_num < len(doc):
                return doc[page_num].get_text()
            return ""
        finally:
            doc.close()

    def get_page_count(self, pdf_path: Path) -> int:
        """Get page count."""
        doc = fitz.open(str(pdf_path))
        try:
            return len(doc)
        finally:
            doc.close()

    def extract_dates_from_page(self, text: str, source: str, page: int):
        """Extract radiocarbon dates from page."""
        for match in self.PATTERNS['c14_full'].finditer(text):
            date_bp = int(match.group(1))
            error = int(match.group(2))

            # Skip implausibly young or old dates for Poverty Point context
            if date_bp < 1000 or date_bp > 10000:
                continue

            ctx = self.get_context(text, match.start(), match.end())

            # Look for lab number nearby
            lab_match = self.PATTERNS['lab_num'].search(ctx)
            lab_num = lab_match.group(1) if lab_match else ""

            # Look for calibrated range
            cal_start, cal_end = None, None
            cal_match = self.PATTERNS['cal_bc'].search(ctx)
            if cal_match:
                cal_start = int(cal_match.group(1))
                cal_end = int(cal_match.group(2))

            # Look for site
            site = ""
            site_match = self.PATTERNS['site_num'].search(ctx)
            if site_match:
                site = site_match.group(1)

            # Look for feature/mound
            feature = ""
            mound_match = self.PATTERNS['mound'].search(ctx)
            if mound_match:
                feature = mound_match.group(1)

            date = C14Date(
                source=source,
                page=page + 1,
                lab_number=lab_num,
                date_bp=date_bp,
                error=error,
                cal_start_bc=cal_start,
                cal_end_bc=cal_end,
                site=site,
                feature=feature,
                raw_text=ctx
            )
            self.dates.append(date)

    def extract_volumes_from_page(self, text: str, source: str, page: int):
        """Extract construction volumes from page."""
        # Check for volume patterns
        for pattern_name, unit in [('vol_m3', 'm³'), ('vol_yd3', 'yd³'), ('vol_ft3', 'ft³')]:
            for match in self.PATTERNS[pattern_name].finditer(text):
                value_str = match.group(1).replace(',', '')
                try:
                    value = float(value_str)
                except ValueError:
                    continue

                # Skip implausibly small values (likely not construction volumes)
                if unit == 'm³' and value < 100:
                    continue
                if unit == 'yd³' and value < 100:
                    continue
                if unit == 'ft³' and value < 1000:
                    continue

                ctx = self.get_context(text, match.start(), match.end())

                # Look for feature name
                feature = ""
                mound_match = self.PATTERNS['mound'].search(ctx)
                if mound_match:
                    feature = mound_match.group(1)
                else:
                    ridge_match = self.PATTERNS['ridge'].search(ctx)
                    if ridge_match:
                        feature = ridge_match.group(1)

                # Convert to cubic meters
                volume_m3 = value * self.UNIT_CONVERSIONS.get(unit, 1.0)

                vol = ConstructionVolume(
                    source=source,
                    page=page + 1,
                    feature=feature,
                    volume_m3=round(volume_m3, 1),
                    original_value=value_str,
                    original_unit=unit,
                    raw_text=ctx
                )
                self.volumes.append(vol)

    def extract_exotics_from_page(self, text: str, source: str, page: int):
        """Extract exotic material references."""
        # Materials and their patterns
        materials = [
            ('copper', 'copper_qty'),
            ('steatite', 'steatite_qty'),
            ('galena', 'galena_qty'),
        ]

        for material_name, pattern_name in materials:
            for match in self.PATTERNS[pattern_name].finditer(text):
                qty = match.group(1)
                ctx = self.get_context(text, match.start(), match.end())

                # Determine source region
                source_region = ""
                if self.PATTERNS['great_lakes'].search(ctx):
                    source_region = "Great Lakes"
                elif self.PATTERNS['appalachian'].search(ctx):
                    source_region = "Appalachian"
                elif self.PATTERNS['ozark'].search(ctx):
                    source_region = "Ozark"

                # Get site
                site = ""
                site_match = self.PATTERNS['site_num'].search(ctx)
                if site_match:
                    site = site_match.group(1)

                exotic = ExoticMaterial(
                    source=source,
                    page=page + 1,
                    material=material_name,
                    quantity=qty,
                    source_region=source_region,
                    site=site,
                    raw_text=ctx
                )
                self.exotics.append(exotic)

    def process_pdf(self, pdf_path: Path, extract_types: list[str]):
        """Process a single PDF."""
        pdf_name = pdf_path.name
        print(f"  Processing: {pdf_name}")

        try:
            page_count = self.get_page_count(pdf_path)
            for page_num in range(page_count):
                text = self.extract_page_text(pdf_path, page_num)

                if 'dates' in extract_types:
                    self.extract_dates_from_page(text, pdf_name, page_num)
                if 'volumes' in extract_types:
                    self.extract_volumes_from_page(text, pdf_name, page_num)
                if 'exotics' in extract_types:
                    self.extract_exotics_from_page(text, pdf_name, page_num)

        except Exception as e:
            print(f"    ERROR: {e}")

    def run_extraction(self, extract_types: list[str], all_pdfs: bool = False):
        """Run targeted extraction."""
        print(f"\nTargeted Data Extraction")
        print(f"{'='*50}")
        print(f"Extracting: {', '.join(extract_types)}")

        # Determine which PDFs to process
        if all_pdfs:
            pdf_files = list(PDF_DIR.glob("*.pdf"))
        else:
            # Use priority PDFs for each extraction type
            pdf_patterns = set()
            for etype in extract_types:
                if etype in PRIORITY_PDFS:
                    pdf_patterns.update(PRIORITY_PDFS[etype])

            pdf_files = []
            for pattern in pdf_patterns:
                pdf_files.extend(PDF_DIR.glob(pattern))
            pdf_files = list(set(pdf_files))  # Remove duplicates

        print(f"PDFs to process: {len(pdf_files)}")

        for pdf_path in sorted(pdf_files):
            self.process_pdf(pdf_path, extract_types)

        print(f"\n{'='*50}")
        print("RESULTS")
        print(f"{'='*50}")
        print(f"Radiocarbon dates: {len(self.dates)}")
        print(f"Construction volumes: {len(self.volumes)}")
        print(f"Exotic materials: {len(self.exotics)}")

    def save_results(self):
        """Save to CSV files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if self.dates:
            path = OUTPUT_DIR / f"c14_dates_targeted_{timestamp}.csv"
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(asdict(self.dates[0]).keys()))
                writer.writeheader()
                for d in self.dates:
                    writer.writerow(asdict(d))
            print(f"Saved: {path}")

        if self.volumes:
            path = OUTPUT_DIR / f"volumes_targeted_{timestamp}.csv"
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(asdict(self.volumes[0]).keys()))
                writer.writeheader()
                for v in self.volumes:
                    writer.writerow(asdict(v))
            print(f"Saved: {path}")

        if self.exotics:
            path = OUTPUT_DIR / f"exotics_targeted_{timestamp}.csv"
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(asdict(self.exotics[0]).keys()))
                writer.writeheader()
                for e in self.exotics:
                    writer.writerow(asdict(e))
            print(f"Saved: {path}")

        # Also save a combined JSON for easy loading
        combined = {
            'extraction_date': datetime.now().isoformat(),
            'dates': [asdict(d) for d in self.dates],
            'volumes': [asdict(v) for v in self.volumes],
            'exotics': [asdict(e) for e in self.exotics],
        }
        json_path = OUTPUT_DIR / f"extracted_data_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(combined, f, indent=2)
        print(f"Saved: {json_path}")


def main():
    parser = argparse.ArgumentParser(description="Targeted PDF data extraction")
    parser.add_argument('--all', action='store_true', help="Process all PDFs (not just priority)")
    parser.add_argument('--dates', action='store_true', help="Extract radiocarbon dates")
    parser.add_argument('--volumes', action='store_true', help="Extract construction volumes")
    parser.add_argument('--exotics', action='store_true', help="Extract exotic materials")

    args = parser.parse_args()

    # Default to all extraction types if none specified
    extract_types = []
    if args.dates:
        extract_types.append('dates')
    if args.volumes:
        extract_types.append('volumes')
    if args.exotics:
        extract_types.append('exotics')

    if not extract_types:
        extract_types = ['dates', 'volumes', 'exotics']

    extractor = TargetedExtractor()
    extractor.run_extraction(extract_types, all_pdfs=args.all)
    extractor.save_results()


if __name__ == "__main__":
    main()
