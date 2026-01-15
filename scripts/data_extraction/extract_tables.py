#!/usr/bin/env python3
"""
Table Extraction Tool for Poverty Point PDFs

Archaeological papers often present radiocarbon dates and other data
in tables. This tool attempts to extract tabular data from PDFs.

Usage:
    python extract_tables.py                    # Process all PDFs
    python extract_tables.py --pdf "Kidder*"    # Process matching PDF
    python extract_tables.py --page 12          # Show specific page
"""

import argparse
import csv
import re
from pathlib import Path
from datetime import datetime

try:
    import pymupdf as fitz
except ImportError:
    import fitz

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
PDF_DIR = PROJECT_ROOT / "pdfs"
OUTPUT_DIR = PROJECT_ROOT / "data" / "extracted" / "tables"


class TableExtractor:
    """Extract tables from PDFs."""

    def __init__(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.extracted_tables = []

    def extract_tables_from_page(self, doc, page_num: int) -> list[dict]:
        """Extract tables from a page using PyMuPDF's table extraction."""
        page = doc[page_num]
        tables = []

        # Try PyMuPDF's built-in table finder (if available in this version)
        try:
            # Get tables using find_tables method
            tab_finder = page.find_tables()
            for tab in tab_finder.tables:
                table_data = tab.extract()
                if table_data and len(table_data) > 1:  # Has header + data
                    tables.append({
                        'page': page_num + 1,
                        'rows': len(table_data),
                        'cols': len(table_data[0]) if table_data else 0,
                        'data': table_data,
                        'bbox': tab.bbox
                    })
        except AttributeError:
            # Older PyMuPDF version - use text-based heuristic
            pass

        return tables

    def identify_c14_table(self, table_data: list[list]) -> bool:
        """Check if table looks like radiocarbon dates."""
        if not table_data or len(table_data) < 2:
            return False

        # Look for keywords in header row
        header_text = ' '.join(str(cell) for cell in table_data[0]).lower()
        c14_keywords = ['date', 'bp', 'b.p.', 'lab', 'beta', 'calibrat', 'sample', 'c14', 'radiocarbon']

        return any(kw in header_text for kw in c14_keywords)

    def parse_c14_table(self, table_data: list[list], source: str, page: int) -> list[dict]:
        """Parse a radiocarbon date table into structured records."""
        if len(table_data) < 2:
            return []

        records = []
        header = [str(h).lower().strip() for h in table_data[0]]

        # Map column indices
        col_map = {}
        for i, h in enumerate(header):
            if 'lab' in h or 'sample' in h or 'number' in h:
                col_map['lab'] = i
            elif 'bp' in h or 'b.p' in h or 'date' in h:
                if 'cal' not in h:
                    col_map['bp'] = i
                else:
                    col_map['cal'] = i
            elif 'material' in h or 'type' in h:
                col_map['material'] = i
            elif 'site' in h or 'provenience' in h or 'context' in h:
                col_map['site'] = i
            elif 'error' in h or '±' in h or 'sigma' in h:
                col_map['error'] = i

        # Parse data rows
        for row in table_data[1:]:
            if not any(str(cell).strip() for cell in row):
                continue  # Skip empty rows

            record = {
                'source': source,
                'page': page,
                'lab_number': '',
                'date_bp': '',
                'error': '',
                'calibrated': '',
                'material': '',
                'site': '',
            }

            for field, idx in col_map.items():
                if idx < len(row):
                    value = str(row[idx]).strip()
                    if field == 'lab':
                        record['lab_number'] = value
                    elif field == 'bp':
                        record['date_bp'] = value
                    elif field == 'error':
                        record['error'] = value
                    elif field == 'cal':
                        record['calibrated'] = value
                    elif field == 'material':
                        record['material'] = value
                    elif field == 'site':
                        record['site'] = value

            # Try to extract BP date from combined cell
            if not record['date_bp'] and col_map.get('bp') is not None:
                cell = str(row[col_map['bp']])
                bp_match = re.search(r'(\d{3,5})\s*[±+-]\s*(\d+)', cell)
                if bp_match:
                    record['date_bp'] = bp_match.group(1)
                    record['error'] = bp_match.group(2)

            if record['date_bp'] or record['lab_number']:
                records.append(record)

        return records

    def extract_text_tables(self, text: str, source: str, page: int) -> list[dict]:
        """
        Extract tables from text using heuristics.
        Looks for patterns like:
        - Aligned columns separated by tabs or multiple spaces
        - Lines with consistent delimiter patterns
        """
        lines = text.split('\n')
        records = []

        # Look for lines that look like radiocarbon data
        # Pattern: lab number + date ± error
        c14_pattern = re.compile(
            r'((?:Beta|GX|Tx|UGa|M|SI|AA|CAMS|I)-?\d+)\s+(\d{3,5})\s*[±+-]\s*(\d+)',
            re.IGNORECASE
        )

        for line in lines:
            match = c14_pattern.search(line)
            if match:
                records.append({
                    'source': source,
                    'page': page,
                    'lab_number': match.group(1),
                    'date_bp': match.group(2),
                    'error': match.group(3),
                    'calibrated': '',
                    'material': '',
                    'site': '',
                    'raw_line': line.strip()
                })

        return records

    def process_pdf(self, pdf_path: Path, verbose: bool = True) -> list[dict]:
        """Process a PDF and extract tables."""
        pdf_name = pdf_path.name
        if verbose:
            print(f"\nProcessing: {pdf_name}")

        all_records = []
        doc = fitz.open(str(pdf_path))

        try:
            for page_num in range(len(doc)):
                # Try structured table extraction
                tables = self.extract_tables_from_page(doc, page_num)

                for table in tables:
                    if self.identify_c14_table(table['data']):
                        records = self.parse_c14_table(table['data'], pdf_name, page_num + 1)
                        if records:
                            if verbose:
                                print(f"  Page {page_num + 1}: Found C14 table with {len(records)} dates")
                            all_records.extend(records)

                # Also try text-based extraction
                text = doc[page_num].get_text()
                text_records = self.extract_text_tables(text, pdf_name, page_num + 1)
                if text_records:
                    if verbose:
                        print(f"  Page {page_num + 1}: Found {len(text_records)} dates in text")
                    all_records.extend(text_records)

        finally:
            doc.close()

        return all_records

    def run(self, pdf_pattern: str = None, verbose: bool = True):
        """Run extraction on PDFs."""
        if pdf_pattern:
            pdf_files = list(PDF_DIR.glob(pdf_pattern))
            if not pdf_files:
                pdf_files = list(PDF_DIR.glob(f"*{pdf_pattern}*"))
        else:
            pdf_files = list(PDF_DIR.glob("*.pdf"))

        print(f"Processing {len(pdf_files)} PDFs...")

        all_records = []
        for pdf_path in sorted(pdf_files):
            records = self.process_pdf(pdf_path, verbose=verbose)
            all_records.extend(records)

        print(f"\n{'='*60}")
        print(f"TOTAL: {len(all_records)} radiocarbon dates extracted")

        if all_records:
            # Remove duplicates based on lab number
            seen = set()
            unique_records = []
            for r in all_records:
                key = (r.get('lab_number', ''), r.get('date_bp', ''))
                if key not in seen and r.get('date_bp'):
                    seen.add(key)
                    unique_records.append(r)

            print(f"UNIQUE: {len(unique_records)} dates after deduplication")

            # Save to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"c14_from_tables_{timestamp}.csv"

            fieldnames = ['source', 'page', 'lab_number', 'date_bp', 'error',
                          'calibrated', 'material', 'site']
            if any('raw_line' in r for r in unique_records):
                fieldnames.append('raw_line')

            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                for r in unique_records:
                    writer.writerow(r)

            print(f"Saved to: {output_path}")

            return unique_records

        return []


def show_page_tables(pdf_pattern: str, page_num: int):
    """Show tables from a specific page."""
    pdf_files = list(PDF_DIR.glob(pdf_pattern))
    if not pdf_files:
        pdf_files = list(PDF_DIR.glob(f"*{pdf_pattern}*"))

    if not pdf_files:
        print(f"No PDF matching '{pdf_pattern}'")
        return

    pdf_path = pdf_files[0]
    doc = fitz.open(str(pdf_path))

    if page_num < 1 or page_num > len(doc):
        print(f"Page {page_num} out of range (1-{len(doc)})")
        doc.close()
        return

    page = doc[page_num - 1]

    print(f"\n{'='*60}")
    print(f"PDF: {pdf_path.name}")
    print(f"Page: {page_num} of {len(doc)}")
    print(f"{'='*60}\n")

    # Try to find tables
    try:
        tab_finder = page.find_tables()
        if tab_finder.tables:
            for i, tab in enumerate(tab_finder.tables):
                data = tab.extract()
                print(f"\nTable {i+1} ({len(data)} rows x {len(data[0]) if data else 0} cols):")
                for row in data[:15]:
                    print(f"  {row}")
                if len(data) > 15:
                    print(f"  ... ({len(data) - 15} more rows)")
        else:
            print("No structured tables found on this page")
    except AttributeError:
        print("Table extraction not available in this PyMuPDF version")

    # Show raw text
    print(f"\n{'='*60}")
    print("Raw text from page:")
    print(f"{'='*60}\n")
    text = page.get_text()
    lines = text.split('\n')
    for i, line in enumerate(lines[:50], 1):
        if line.strip():
            print(f"{i:3d} | {line}")
    if len(lines) > 50:
        print(f"... ({len(lines) - 50} more lines)")

    doc.close()


def main():
    parser = argparse.ArgumentParser(description="Extract tables from PDFs")
    parser.add_argument('--pdf', '-p', help="PDF pattern to process")
    parser.add_argument('--page', type=int, help="Show specific page tables")
    parser.add_argument('--quiet', '-q', action='store_true', help="Reduce output")

    args = parser.parse_args()

    if args.page and args.pdf:
        show_page_tables(args.pdf, args.page)
    else:
        extractor = TableExtractor()
        extractor.run(pdf_pattern=args.pdf, verbose=not args.quiet)


if __name__ == "__main__":
    main()
