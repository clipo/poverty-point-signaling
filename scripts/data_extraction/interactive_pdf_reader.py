#!/usr/bin/env python3
"""
Interactive PDF Reader for Poverty Point Project

This tool lets you explore PDF content page-by-page without hitting
context limits. It extracts text from individual pages and saves
sections you mark as relevant.

Usage:
    python interactive_pdf_reader.py                    # List PDFs
    python interactive_pdf_reader.py --pdf "Kidder*"    # Open matching PDF
    python interactive_pdf_reader.py --search "date"    # Search across PDFs

Commands during interactive mode:
    n / next      - Go to next page
    p / prev      - Go to previous page
    g 10          - Go to page 10
    s / save      - Save current page text to notes
    f "pattern"   - Find pattern on current page
    /pattern      - Search all pages for pattern
    q / quit      - Exit

The tool saves extracted text to data/extracted/notes/ for later review.
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    import pymupdf as fitz
except ImportError:
    import fitz

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
PDF_DIR = PROJECT_ROOT / "pdfs"
NOTES_DIR = PROJECT_ROOT / "data" / "extracted" / "notes"


class InteractivePDFReader:
    """Interactive PDF exploration tool."""

    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(str(pdf_path))
        self.current_page = 0
        self.total_pages = len(self.doc)
        self.saved_notes: list[dict] = []
        NOTES_DIR.mkdir(parents=True, exist_ok=True)

    def get_page_text(self, page_num: int) -> str:
        """Get text from a page."""
        if 0 <= page_num < self.total_pages:
            return self.doc[page_num].get_text()
        return ""

    def display_page(self, page_num: int, max_lines: int = 50):
        """Display a page's content."""
        text = self.get_page_text(page_num)
        lines = text.split('\n')

        print(f"\n{'='*60}")
        print(f"PDF: {self.pdf_path.name}")
        print(f"Page {page_num + 1} of {self.total_pages}")
        print(f"{'='*60}\n")

        for i, line in enumerate(lines[:max_lines]):
            if line.strip():
                print(f"{i+1:3d} | {line[:100]}")

        if len(lines) > max_lines:
            print(f"\n... ({len(lines) - max_lines} more lines)")

    def find_in_page(self, pattern: str, page_num: int) -> list[tuple[int, str]]:
        """Find pattern in a page, return (line_num, line) tuples."""
        text = self.get_page_text(page_num)
        lines = text.split('\n')
        matches = []

        try:
            regex = re.compile(pattern, re.IGNORECASE)
            for i, line in enumerate(lines):
                if regex.search(line):
                    matches.append((i + 1, line))
        except re.error:
            # Fall back to simple string search
            for i, line in enumerate(lines):
                if pattern.lower() in line.lower():
                    matches.append((i + 1, line))

        return matches

    def search_all_pages(self, pattern: str) -> dict[int, list[tuple[int, str]]]:
        """Search all pages for pattern."""
        results = {}
        for page_num in range(self.total_pages):
            matches = self.find_in_page(pattern, page_num)
            if matches:
                results[page_num] = matches
        return results

    def save_current_page(self, note: str = ""):
        """Save current page to notes."""
        text = self.get_page_text(self.current_page)
        self.saved_notes.append({
            'pdf': self.pdf_path.name,
            'page': self.current_page + 1,
            'note': note,
            'text': text,
            'timestamp': datetime.now().isoformat()
        })
        print(f"Saved page {self.current_page + 1} to notes (total: {len(self.saved_notes)})")

    def export_notes(self):
        """Export saved notes to file."""
        if not self.saved_notes:
            print("No notes to export")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_stem = self.pdf_path.stem[:30]  # Truncate long names
        output_path = NOTES_DIR / f"notes_{pdf_stem}_{timestamp}.txt"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"PDF Notes Export\n")
            f.write(f"Source: {self.pdf_path.name}\n")
            f.write(f"Exported: {datetime.now().isoformat()}\n")
            f.write(f"{'='*60}\n\n")

            for note in self.saved_notes:
                f.write(f"--- Page {note['page']} ---\n")
                if note['note']:
                    f.write(f"Note: {note['note']}\n")
                f.write(f"\n{note['text']}\n")
                f.write(f"\n{'='*60}\n\n")

        print(f"Exported {len(self.saved_notes)} notes to: {output_path}")

    def run_interactive(self):
        """Run interactive mode."""
        self.display_page(self.current_page)

        while True:
            try:
                cmd = input(f"\n[Page {self.current_page + 1}/{self.total_pages}] Command (h for help): ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not cmd:
                continue

            # Parse command
            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if action in ('q', 'quit', 'exit'):
                if self.saved_notes:
                    self.export_notes()
                break

            elif action in ('h', 'help', '?'):
                self.show_help()

            elif action in ('n', 'next'):
                if self.current_page < self.total_pages - 1:
                    self.current_page += 1
                    self.display_page(self.current_page)
                else:
                    print("Already at last page")

            elif action in ('p', 'prev', 'previous'):
                if self.current_page > 0:
                    self.current_page -= 1
                    self.display_page(self.current_page)
                else:
                    print("Already at first page")

            elif action in ('g', 'goto'):
                try:
                    page = int(arg) - 1  # Convert to 0-indexed
                    if 0 <= page < self.total_pages:
                        self.current_page = page
                        self.display_page(self.current_page)
                    else:
                        print(f"Page must be 1-{self.total_pages}")
                except ValueError:
                    print("Usage: g <page_number>")

            elif action in ('s', 'save'):
                self.save_current_page(arg)

            elif action in ('f', 'find'):
                if arg:
                    matches = self.find_in_page(arg, self.current_page)
                    if matches:
                        print(f"\nFound {len(matches)} matches on this page:")
                        for line_num, line in matches[:20]:
                            print(f"  {line_num:3d}: {line[:80]}")
                    else:
                        print(f"No matches for '{arg}' on this page")
                else:
                    print("Usage: f <pattern>")

            elif action.startswith('/'):
                # Search all pages
                pattern = cmd[1:]
                if pattern:
                    results = self.search_all_pages(pattern)
                    if results:
                        print(f"\nFound matches on {len(results)} pages:")
                        for page_num, matches in sorted(results.items())[:10]:
                            print(f"\n  Page {page_num + 1}:")
                            for line_num, line in matches[:3]:
                                print(f"    {line_num}: {line[:60]}...")
                        if len(results) > 10:
                            print(f"\n  ... and {len(results) - 10} more pages")
                    else:
                        print(f"No matches for '{pattern}'")
                else:
                    print("Usage: /pattern")

            elif action in ('r', 'refresh'):
                self.display_page(self.current_page)

            elif action in ('x', 'export'):
                self.export_notes()

            elif action in ('all', 'full'):
                # Show full page without line limit
                text = self.get_page_text(self.current_page)
                print(f"\n{'='*60}")
                print(f"Page {self.current_page + 1} - Full Text")
                print(f"{'='*60}\n")
                print(text)

            else:
                print(f"Unknown command: {action} (type 'h' for help)")

        self.doc.close()

    def show_help(self):
        """Show help message."""
        print("""
Commands:
  n / next        Go to next page
  p / prev        Go to previous page
  g <num>         Go to page number
  s [note]        Save current page (with optional note)
  f <pattern>     Find pattern on current page
  /<pattern>      Search all pages for pattern
  all             Show full page text (no truncation)
  x / export      Export saved notes to file
  r / refresh     Redisplay current page
  h / help        Show this help
  q / quit        Exit (auto-exports notes)
        """)


def list_pdfs():
    """List available PDFs."""
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    print(f"\nAvailable PDFs in {PDF_DIR}:\n")
    for i, pdf in enumerate(pdfs, 1):
        size_mb = pdf.stat().st_size / (1024 * 1024)
        doc = fitz.open(str(pdf))
        pages = len(doc)
        doc.close()
        print(f"  {i:2d}. {pdf.name}")
        print(f"      {size_mb:.1f} MB, {pages} pages")
    print()


def search_all_pdfs(pattern: str):
    """Search across all PDFs."""
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    print(f"\nSearching for '{pattern}' across {len(pdfs)} PDFs...\n")

    for pdf_path in pdfs:
        doc = fitz.open(str(pdf_path))
        pdf_matches = []

        for page_num in range(len(doc)):
            text = doc[page_num].get_text()
            if re.search(pattern, text, re.IGNORECASE):
                # Count matches on this page
                count = len(re.findall(pattern, text, re.IGNORECASE))
                pdf_matches.append((page_num + 1, count))

        doc.close()

        if pdf_matches:
            total = sum(c for _, c in pdf_matches)
            print(f"{pdf_path.name}:")
            print(f"  {total} matches on pages: {[p for p, _ in pdf_matches[:10]]}")
            if len(pdf_matches) > 10:
                print(f"  ... and {len(pdf_matches) - 10} more pages")
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Interactive PDF reader for archaeological research"
    )
    parser.add_argument(
        '--pdf', '-p',
        help="PDF file pattern (e.g., 'Kidder*')"
    )
    parser.add_argument(
        '--search', '-s',
        help="Search pattern across all PDFs"
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help="List available PDFs"
    )

    args = parser.parse_args()

    if args.list or (not args.pdf and not args.search):
        list_pdfs()
        return

    if args.search:
        search_all_pdfs(args.search)
        return

    if args.pdf:
        # Find matching PDF
        matches = list(PDF_DIR.glob(args.pdf))
        if not matches:
            # Try with .pdf extension
            matches = list(PDF_DIR.glob(f"{args.pdf}*.pdf"))

        if not matches:
            print(f"No PDFs matching '{args.pdf}'")
            list_pdfs()
            return

        if len(matches) > 1:
            print(f"Multiple matches for '{args.pdf}':")
            for m in matches:
                print(f"  {m.name}")
            print("\nPlease be more specific")
            return

        reader = InteractivePDFReader(matches[0])
        reader.run_interactive()


if __name__ == "__main__":
    main()
