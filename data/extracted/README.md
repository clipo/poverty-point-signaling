# PDF Data Extraction Tools

This directory contains data extracted from archaeological PDFs using the scripts in `scripts/data_extraction/`.

## Available Scripts

### 1. `extract_pdf_data.py` - General Extraction
Extracts multiple data types using regex patterns:
- Radiocarbon dates (BP dates with errors)
- Construction measurements (volumes, heights)
- Exotic goods references (copper, steatite, galena)
- Site references (Louisiana/Mississippi trinomials)

```bash
# Process all PDFs
python scripts/data_extraction/extract_pdf_data.py

# Process specific PDF
python scripts/data_extraction/extract_pdf_data.py --pdf "Kidder*"

# Quick summary only
python scripts/data_extraction/extract_pdf_data.py --summary
```

### 2. `extract_specific_data.py` - Targeted Extraction
More selective extraction with improved parsing:
- Filters plausible date ranges (1000-10000 BP for Poverty Point context)
- Converts volume units to cubic meters
- Associates exotic materials with source regions

```bash
# Extract all data types from priority PDFs
python scripts/data_extraction/extract_specific_data.py

# Extract only radiocarbon dates
python scripts/data_extraction/extract_specific_data.py --dates

# Process all PDFs (not just priority)
python scripts/data_extraction/extract_specific_data.py --all
```

### 3. `interactive_pdf_reader.py` - Manual Review
Interactive tool for exploring PDFs page-by-page:
- Navigate pages with `n`/`p` commands
- Search within pages with `f pattern`
- Search across all pages with `/pattern`
- Save relevant pages to notes

```bash
# List available PDFs
python scripts/data_extraction/interactive_pdf_reader.py --list

# Open specific PDF
python scripts/data_extraction/interactive_pdf_reader.py --pdf "Webb-1956"

# Search across all PDFs
python scripts/data_extraction/interactive_pdf_reader.py --search "radiocarbon"
```

### 4. `extract_tables.py` - Table Extraction
Attempts to extract structured tables (works best with modern PDFs):

```bash
python scripts/data_extraction/extract_tables.py
python scripts/data_extraction/extract_tables.py --pdf "Kidder*" --page 12
```

## Key Data Extracted

### Construction Volumes
From Kidder 2006:
- **750,000 m³** total earthwork at Poverty Point (16WC5)

### Exotic Materials (from Webb 1956, Hays 2018)
At Poverty Point:
- **155 copper objects**
- **2,221 steatite objects**
- **702 galena objects**
- **~3,000 steatite vessel fragments**

### Chronology
- Poverty Point occupation: ca. 3600-3100 cal BP (1700-1100 BCE)
- Regional hiatus: ca. 3100-2500 cal BP

## Output Files

Extracted data is saved with timestamps:
- `radiocarbon_dates_YYYYMMDD_HHMMSS.csv`
- `measurements_YYYYMMDD_HHMMSS.csv`
- `exotic_goods_YYYYMMDD_HHMMSS.csv`
- `site_references_YYYYMMDD_HHMMSS.csv`
- `extracted_data_YYYYMMDD_HHMMSS.json` (combined)

## Notes Directory

Manual notes saved from interactive reader are in `notes/`.

## Known Limitations

1. **Scanned PDFs**: Older archaeological papers are often scanned images where text extraction quality varies
2. **Table extraction**: Works best with modern PDFs with proper structure; older PDFs may require manual review
3. **Context ambiguity**: Regex patterns may capture false positives (e.g., page numbers that look like dates)

## Recommended Workflow

1. Run `extract_pdf_data.py --summary` to understand PDF contents
2. Run `extract_specific_data.py --all` for automated extraction
3. Use `interactive_pdf_reader.py` to manually review key pages
4. Cross-reference with original PDFs for validation
