#!/usr/bin/env python3
"""
PDF Data Extraction Tool for Poverty Point Project

Extracts structured data from archaeological PDFs without loading entire
documents into memory at once. Outputs CSV files for:
- Radiocarbon dates
- Construction volumes/measurements
- Exotic goods data
- Site locations and sizes

Usage:
    python extract_pdf_data.py                    # Process all PDFs
    python extract_pdf_data.py --pdf "Kidder*"    # Process matching PDFs
    python extract_pdf_data.py --summary          # Quick summary of each PDF
"""

import argparse
import csv
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict

# Try to import PDF libraries
try:
    import pymupdf as fitz  # PyMuPDF (newer import name)
except ImportError:
    try:
        import fitz  # PyMuPDF (older import name)
    except ImportError:
        fitz = None

try:
    from pdfminer.high_level import extract_text_by_page
    from pdfminer.pdfpage import PDFPage
except ImportError:
    extract_text_by_page = None


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
PDF_DIR = PROJECT_ROOT / "pdfs"
OUTPUT_DIR = PROJECT_ROOT / "data" / "extracted"


@dataclass
class RadiocarbonDate:
    """Structured radiocarbon date entry."""
    source_pdf: str
    page_number: int
    lab_number: str = ""
    raw_date_bp: str = ""
    error_plus_minus: str = ""
    calibrated_range: str = ""
    material: str = ""
    provenience: str = ""
    context: str = ""  # Surrounding text for verification


@dataclass
class ConstructionMeasurement:
    """Construction volume or measurement."""
    source_pdf: str
    page_number: int
    feature: str = ""  # e.g., "Mound A", "Ridge 1"
    measurement_type: str = ""  # volume, height, area, etc.
    value: str = ""
    unit: str = ""
    context: str = ""


@dataclass
class ExoticGood:
    """Exotic material or artifact."""
    source_pdf: str
    page_number: int
    material: str = ""  # copper, steatite, galena, etc.
    source_location: str = ""
    quantity: str = ""
    artifact_type: str = ""
    context: str = ""


@dataclass
class SiteReference:
    """Archaeological site reference."""
    source_pdf: str
    page_number: int
    site_name: str = ""
    site_number: str = ""  # Trinomial (e.g., 16WC5)
    location: str = ""
    size_info: str = ""
    context: str = ""


class PDFExtractor:
    """Extract structured data from archaeological PDFs."""

    # Regex patterns for data extraction
    PATTERNS = {
        # Radiocarbon dates: various formats
        'c14_bp': re.compile(
            r'(\d{3,5})\s*[±+/-]\s*(\d{1,4})\s*(?:B\.?P\.?|bp|years?\s*(?:before\s*present)?)',
            re.IGNORECASE
        ),
        'lab_number': re.compile(
            r'((?:Beta|GX|M|SI|Tx|UGa|ISGS|AA|CAMS|OxA|Wk|ETH|UCIAMS|OS|NOSAMS|I)-?\d{3,6})',
            re.IGNORECASE
        ),
        'cal_range': re.compile(
            r'(?:cal(?:ibrated)?\.?\s*)?(\d{3,4})\s*[-–—to]\s*(\d{3,4})\s*(?:cal\.?\s*)?(?:B\.?C\.?E?\.?|BCE|BC|A\.?D\.?)',
            re.IGNORECASE
        ),

        # Measurements
        'volume_m3': re.compile(
            r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:cubic\s*)?(?:m(?:eters?)?³|m3|cu\.?\s*m)',
            re.IGNORECASE
        ),
        'volume_ft3': re.compile(
            r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:cubic\s*)?(?:ft|feet|foot)(?:³|3)?',
            re.IGNORECASE
        ),
        'height_m': re.compile(
            r'(\d+(?:\.\d+)?)\s*(?:m(?:eters?)?|metres?)\s*(?:high|tall|in\s*height)',
            re.IGNORECASE
        ),

        # Exotic materials
        'copper': re.compile(
            r'(copper|native\s*copper)',
            re.IGNORECASE
        ),
        'steatite': re.compile(
            r'(steatite|soapstone)',
            re.IGNORECASE
        ),
        'galena': re.compile(
            r'(galena|lead\s*ore)',
            re.IGNORECASE
        ),
        'crystal': re.compile(
            r'(quartz\s*crystal|rock\s*crystal)',
            re.IGNORECASE
        ),

        # Site numbers (Louisiana trinomial format)
        'site_trinomial': re.compile(
            r'(16[A-Z]{2}\d{1,4})',
            re.IGNORECASE
        ),
    }

    def __init__(self, pdf_dir: Path = PDF_DIR, output_dir: Path = OUTPUT_DIR):
        self.pdf_dir = pdf_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Storage for extracted data
        self.radiocarbon_dates: list[RadiocarbonDate] = []
        self.measurements: list[ConstructionMeasurement] = []
        self.exotic_goods: list[ExoticGood] = []
        self.site_references: list[SiteReference] = []

        # Check which PDF library is available
        if fitz is not None:
            self.pdf_backend = 'pymupdf'
        elif extract_text_by_page is not None:
            self.pdf_backend = 'pdfminer'
        else:
            self.pdf_backend = None
            print("WARNING: No PDF library found. Install with:")
            print("  pip install pymupdf")
            print("  OR")
            print("  pip install pdfminer.six")

    def get_pdf_files(self, pattern: Optional[str] = None) -> list[Path]:
        """Get list of PDF files, optionally filtered by pattern."""
        if pattern:
            return list(self.pdf_dir.glob(pattern))
        return list(self.pdf_dir.glob("*.pdf"))

    def extract_text_from_page_pymupdf(self, pdf_path: Path, page_num: int) -> str:
        """Extract text from a single page using PyMuPDF."""
        doc = fitz.open(str(pdf_path))
        try:
            if page_num < len(doc):
                page = doc[page_num]
                return page.get_text()
            return ""
        finally:
            doc.close()

    def get_page_count_pymupdf(self, pdf_path: Path) -> int:
        """Get number of pages using PyMuPDF."""
        doc = fitz.open(str(pdf_path))
        try:
            return len(doc)
        finally:
            doc.close()

    def extract_text_from_page_pdfminer(self, pdf_path: Path, page_num: int) -> str:
        """Extract text from a single page using pdfminer."""
        with open(pdf_path, 'rb') as f:
            for i, page in enumerate(PDFPage.get_pages(f)):
                if i == page_num:
                    # This is a simplification - pdfminer works differently
                    from pdfminer.high_level import extract_text
                    return extract_text(pdf_path, page_numbers=[page_num])
        return ""

    def extract_page_text(self, pdf_path: Path, page_num: int) -> str:
        """Extract text from a page using available backend."""
        if self.pdf_backend == 'pymupdf':
            return self.extract_text_from_page_pymupdf(pdf_path, page_num)
        elif self.pdf_backend == 'pdfminer':
            return self.extract_text_from_page_pdfminer(pdf_path, page_num)
        else:
            raise RuntimeError("No PDF library available")

    def get_page_count(self, pdf_path: Path) -> int:
        """Get number of pages in PDF."""
        if self.pdf_backend == 'pymupdf':
            return self.get_page_count_pymupdf(pdf_path)
        elif self.pdf_backend == 'pdfminer':
            with open(pdf_path, 'rb') as f:
                return sum(1 for _ in PDFPage.get_pages(f))
        else:
            raise RuntimeError("No PDF library available")

    def get_context(self, text: str, match_start: int, match_end: int,
                    context_chars: int = 150) -> str:
        """Get surrounding context for a match."""
        start = max(0, match_start - context_chars)
        end = min(len(text), match_end + context_chars)
        context = text[start:end]
        # Clean up whitespace
        context = ' '.join(context.split())
        return f"...{context}..."

    def extract_radiocarbon_dates(self, text: str, pdf_name: str, page_num: int):
        """Extract radiocarbon dates from page text."""
        # Find BP dates
        for match in self.PATTERNS['c14_bp'].finditer(text):
            date = RadiocarbonDate(
                source_pdf=pdf_name,
                page_number=page_num + 1,  # 1-indexed for human readability
                raw_date_bp=match.group(1),
                error_plus_minus=match.group(2),
                context=self.get_context(text, match.start(), match.end())
            )

            # Try to find associated lab number nearby
            search_start = max(0, match.start() - 200)
            search_end = min(len(text), match.end() + 200)
            nearby_text = text[search_start:search_end]

            lab_match = self.PATTERNS['lab_number'].search(nearby_text)
            if lab_match:
                date.lab_number = lab_match.group(1)

            # Try to find calibrated range
            cal_match = self.PATTERNS['cal_range'].search(nearby_text)
            if cal_match:
                date.calibrated_range = f"{cal_match.group(1)}-{cal_match.group(2)}"

            self.radiocarbon_dates.append(date)

    def extract_measurements(self, text: str, pdf_name: str, page_num: int):
        """Extract construction measurements from page text."""
        # Volume in cubic meters
        for match in self.PATTERNS['volume_m3'].finditer(text):
            meas = ConstructionMeasurement(
                source_pdf=pdf_name,
                page_number=page_num + 1,
                measurement_type="volume",
                value=match.group(1).replace(',', ''),
                unit="m³",
                context=self.get_context(text, match.start(), match.end())
            )
            self.measurements.append(meas)

        # Volume in cubic feet
        for match in self.PATTERNS['volume_ft3'].finditer(text):
            meas = ConstructionMeasurement(
                source_pdf=pdf_name,
                page_number=page_num + 1,
                measurement_type="volume",
                value=match.group(1).replace(',', ''),
                unit="ft³",
                context=self.get_context(text, match.start(), match.end())
            )
            self.measurements.append(meas)

    def extract_exotic_goods(self, text: str, pdf_name: str, page_num: int):
        """Extract exotic goods references from page text."""
        exotic_patterns = ['copper', 'steatite', 'galena', 'crystal']

        for pattern_name in exotic_patterns:
            for match in self.PATTERNS[pattern_name].finditer(text):
                exotic = ExoticGood(
                    source_pdf=pdf_name,
                    page_number=page_num + 1,
                    material=match.group(1),
                    context=self.get_context(text, match.start(), match.end())
                )
                self.exotic_goods.append(exotic)

    def extract_site_references(self, text: str, pdf_name: str, page_num: int):
        """Extract site references from page text."""
        for match in self.PATTERNS['site_trinomial'].finditer(text):
            site = SiteReference(
                source_pdf=pdf_name,
                page_number=page_num + 1,
                site_number=match.group(1),
                context=self.get_context(text, match.start(), match.end())
            )
            self.site_references.append(site)

    def process_pdf(self, pdf_path: Path, verbose: bool = True):
        """Process a single PDF file, page by page."""
        pdf_name = pdf_path.name

        if verbose:
            print(f"\nProcessing: {pdf_name}")

        try:
            page_count = self.get_page_count(pdf_path)
            if verbose:
                print(f"  Pages: {page_count}")

            for page_num in range(page_count):
                text = self.extract_page_text(pdf_path, page_num)

                # Run all extractors on this page
                self.extract_radiocarbon_dates(text, pdf_name, page_num)
                self.extract_measurements(text, pdf_name, page_num)
                self.extract_exotic_goods(text, pdf_name, page_num)
                self.extract_site_references(text, pdf_name, page_num)

                if verbose and (page_num + 1) % 10 == 0:
                    print(f"  Processed page {page_num + 1}/{page_count}")

            if verbose:
                print(f"  Complete: {pdf_name}")

        except Exception as e:
            print(f"  ERROR processing {pdf_name}: {e}")

    def process_all_pdfs(self, pattern: Optional[str] = None, verbose: bool = True):
        """Process all PDFs (or those matching pattern)."""
        pdf_files = self.get_pdf_files(pattern)

        if not pdf_files:
            print(f"No PDF files found in {self.pdf_dir}")
            return

        print(f"Found {len(pdf_files)} PDF files to process")

        for pdf_path in sorted(pdf_files):
            self.process_pdf(pdf_path, verbose=verbose)

        print(f"\n{'='*60}")
        print("EXTRACTION SUMMARY")
        print(f"{'='*60}")
        print(f"Radiocarbon dates found: {len(self.radiocarbon_dates)}")
        print(f"Measurements found: {len(self.measurements)}")
        print(f"Exotic goods references: {len(self.exotic_goods)}")
        print(f"Site references: {len(self.site_references)}")

    def save_results(self):
        """Save extracted data to CSV files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save radiocarbon dates
        if self.radiocarbon_dates:
            output_path = self.output_dir / f"radiocarbon_dates_{timestamp}.csv"
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(asdict(self.radiocarbon_dates[0]).keys()))
                writer.writeheader()
                for date in self.radiocarbon_dates:
                    writer.writerow(asdict(date))
            print(f"Saved: {output_path}")

        # Save measurements
        if self.measurements:
            output_path = self.output_dir / f"measurements_{timestamp}.csv"
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(asdict(self.measurements[0]).keys()))
                writer.writeheader()
                for meas in self.measurements:
                    writer.writerow(asdict(meas))
            print(f"Saved: {output_path}")

        # Save exotic goods
        if self.exotic_goods:
            output_path = self.output_dir / f"exotic_goods_{timestamp}.csv"
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(asdict(self.exotic_goods[0]).keys()))
                writer.writeheader()
                for exotic in self.exotic_goods:
                    writer.writerow(asdict(exotic))
            print(f"Saved: {output_path}")

        # Save site references
        if self.site_references:
            output_path = self.output_dir / f"site_references_{timestamp}.csv"
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(asdict(self.site_references[0]).keys()))
                writer.writeheader()
                for site in self.site_references:
                    writer.writerow(asdict(site))
            print(f"Saved: {output_path}")

        # Save combined summary
        summary_path = self.output_dir / f"extraction_summary_{timestamp}.txt"
        with open(summary_path, 'w') as f:
            f.write(f"PDF Data Extraction Summary\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"Radiocarbon dates: {len(self.radiocarbon_dates)}\n")
            f.write(f"Measurements: {len(self.measurements)}\n")
            f.write(f"Exotic goods references: {len(self.exotic_goods)}\n")
            f.write(f"Site references: {len(self.site_references)}\n")
        print(f"Saved: {summary_path}")

    def generate_summary(self, pattern: Optional[str] = None):
        """Generate quick summary of PDFs without full extraction."""
        pdf_files = self.get_pdf_files(pattern)

        print(f"\n{'='*60}")
        print("PDF LIBRARY SUMMARY")
        print(f"{'='*60}\n")

        for pdf_path in sorted(pdf_files):
            try:
                page_count = self.get_page_count(pdf_path)
                size_mb = pdf_path.stat().st_size / (1024 * 1024)
                print(f"{pdf_path.name}")
                print(f"  Size: {size_mb:.1f} MB | Pages: {page_count}")

                # Sample first page for quick content check
                first_page = self.extract_page_text(pdf_path, 0)
                # Count potential hits
                c14_count = len(self.PATTERNS['c14_bp'].findall(first_page))
                site_count = len(self.PATTERNS['site_trinomial'].findall(first_page))

                if c14_count > 0 or site_count > 0:
                    print(f"  Page 1 preview: ~{c14_count} dates, ~{site_count} site refs")
                print()

            except Exception as e:
                print(f"{pdf_path.name}: ERROR - {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured data from archaeological PDFs"
    )
    parser.add_argument(
        '--pdf', '-p',
        help="Glob pattern to filter PDFs (e.g., 'Kidder*')"
    )
    parser.add_argument(
        '--summary', '-s',
        action='store_true',
        help="Just generate summary, don't extract data"
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=OUTPUT_DIR,
        help="Output directory for CSV files"
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help="Reduce output verbosity"
    )

    args = parser.parse_args()

    extractor = PDFExtractor(output_dir=args.output)

    if extractor.pdf_backend is None:
        print("\nERROR: No PDF library available.")
        print("Please install one of:")
        print("  pip install pymupdf")
        print("  pip install pdfminer.six")
        sys.exit(1)

    print(f"Using PDF backend: {extractor.pdf_backend}")

    if args.summary:
        extractor.generate_summary(args.pdf)
    else:
        extractor.process_all_pdfs(pattern=args.pdf, verbose=not args.quiet)
        extractor.save_results()


if __name__ == "__main__":
    main()
