# Quick Reference - Kantec to Paxton 10 Converter

## Quick Start

### Single Card Conversion
```bash
python3 kantec_to_paxton_converter.py "4D:52042"
```

### CSV File Conversion
```bash
python3 kantec_to_paxton_converter.py --csv input.csv output.csv
```

## Format Examples

| Kantec | Paxton 10 |
|--------|-----------|
| `4D:52042` | `9716ABCDEFZ82Z014ACB4D139716` |
| `35:46655` | `9716ABCDEFZ82Z013FB635179716` |

## CSV File Format

**Input (must have 'Kantec' column):**
```csv
Name,Department,Kantec
John Smith,IT,4D:52042
Jane Doe,HR,35:46655
```

**Output (adds 'Paxton' column):**
```csv
Name,Department,Kantec,Paxton
John Smith,IT,4D:52042,9716ABCDEFZ82Z014ACB4D139716
Jane Doe,HR,35:46655,9716ABCDEFZ82Z013FB635179716
```

## Validation

Run without arguments to test the converter:
```bash
python3 kantec_to_paxton_converter.py
```

This will verify the conversion against your two known examples.

## Important Notes

- ✓ Tested and verified with your provided examples
- ✓ Handles errors gracefully
- ✓ Preserves all original CSV columns
- ⚠ Test a few cards on your Paxton 10 system before full migration
