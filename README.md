# Kantec-to-Paxton10-Card-Converter
Kantec to Paxton10 Card Converter


# Kantec to Paxton 10 Card Number Converter

This package contains everything you need to convert card numbers from your Kantec EntraPass Special Edition system to Paxton 10 format.

## What's Included

- **`kantec_to_paxton_converter.py`** - The main conversion script
- **`CONVERSION_GUIDE.md`** - Comprehensive guide with technical details
- **`QUICK_REFERENCE.md`** - Quick start guide for immediate use
- **`example_kantec_cards.csv`** - Sample input file
- **`example_paxton_cards.csv`** - Sample output file showing converted results

## Verified Results

The converter has been tested against your provided examples and produces **exact matches**:

✓ **Card A**: `4D:52042` → `9716ABCDEFZ82Z014ACB4D139716`  
✓ **Card B**: `35:46655` → `9716ABCDEFZ82Z013FB635179716`

## Quick Start

### Test the Converter
```bash
python3 kantec_to_paxton_converter.py
```

### Convert Your CSV File
```bash
python3 kantec_to_paxton_converter.py --csv your_cards.csv output_cards.csv
```

## Requirements

- Python 3.x (already installed on most systems)
- No additional packages required

## Documentation

- For detailed instructions, see **`CONVERSION_GUIDE.md`**
- For quick reference, see **`QUICK_REFERENCE.md`**

## How It Works

The converter analyzes the Kantec format (`XX:XXXXX`) and encodes it into the Paxton 10 format using the discovered encoding structure:

1. Parses the facility code (hex) and card number (decimal)
2. Encodes them into a 9-byte structure
3. Calculates the checksum
4. Formats the output with the Paxton 10 wrapper

## Support

If you have any questions or encounter issues:
1. Check the `CONVERSION_GUIDE.md` for troubleshooting
2. Verify your input format matches the examples
3. Test with the provided example files first

---

**Created**: November 2025  
**Status**: Tested and verified with real card data
