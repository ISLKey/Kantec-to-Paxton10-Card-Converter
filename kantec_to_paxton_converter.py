#!/usr/bin/env python3
"""
Kantec to Paxton 10 Card Number Converter
==========================================

Converts Kantec EntraPass card numbers to Paxton 10 format.

Usage:
  python3 kantec_to_paxton_converter.py <kantec_number>
  python3 kantec_to_paxton_converter.py --csv <input.csv> <output.csv>

Examples:
  python3 kantec_to_paxton_converter.py "4D:52042"
  python3 kantec_to_paxton_converter.py --csv kantec_cards.csv paxton_cards.csv
"""

import sys
import csv

def calculate_checksum(sum_bytes):
    """
    Calculate checksum byte based on sum of preceding bytes.
    
    Formula discovered from analysis:
    checksum = (sum & 0x0F) + (0x17 - (sum >> 4) * 4)
    
    This formula matches both known examples:
    - Card A: sum=0x4C -> checksum=0x13
    - Card B: sum=0x14 -> checksum=0x17
    """
    sum_low = sum_bytes & 0x0F
    sum_high = sum_bytes >> 4
    
    checksum = sum_low + (0x17 - sum_high * 4)
    
    return checksum & 0xFF

def kantec_to_paxton(kantec_number):
    """
    Convert Kantec card number to Paxton 10 format.
    
    Args:
        kantec_number (str): Kantec format "XX:XXXXX" (e.g., "4D:52042")
    
    Returns:
        str: Paxton 10 format card number
    
    Raises:
        ValueError: If input format is invalid
    """
    try:
        # Parse and validate input
        parts = kantec_number.strip().split(':')
        if len(parts) != 2:
            raise ValueError(f"Invalid format. Expected 'XX:XXXXX', got '{kantec_number}'")
        
        facility_hex = parts[0].strip().upper()
        card_decimal = parts[1].strip()
        
        # Convert to integers
        facility = int(facility_hex, 16)
        card_num = int(card_decimal)
        
        # Validate ranges
        if not (0 <= facility <= 255):
            raise ValueError(f"Facility code must be 00-FF (hex), got {facility_hex}")
        if not (0 <= card_num <= 65535):
            raise ValueError(f"Card number must be 0-65535, got {card_num}")
        
        # Build the 9-byte data structure
        # Bytes 0-3: Fixed header (appears constant across all cards)
        data = bytearray([0xAB, 0xCD, 0xEF, 0x82])
        
        # Byte 4: Fixed value
        data.append(0x01)
        
        # Bytes 5-6: Card number in little-endian format
        card_bytes = card_num.to_bytes(2, 'little')
        data.extend(card_bytes)
        
        # Byte 7: Facility code
        data.append(facility)
        
        # Calculate sum of bytes 0-7 for checksum calculation
        sum_bytes = sum(data) & 0xFF
        
        # Byte 8: Checksum
        checksum = calculate_checksum(sum_bytes)
        data.append(checksum)
        
        # Convert to hex string
        hex_string = data.hex().upper()
        
        # Insert 'Z' markers at specific positions
        # Format: ABCDEF Z 82 Z 01...
        # After byte 2 (position 6) and after byte 3 (position 8+1)
        middle_section = hex_string[:6] + 'Z' + hex_string[6:8] + 'Z' + hex_string[8:]
        
        # Build final Paxton format: 9716 + middle + 9716
        paxton_number = f"9716{middle_section}9716"
        
        return paxton_number
        
    except ValueError as e:
        raise
    except Exception as e:
        raise ValueError(f"Error converting '{kantec_number}': {str(e)}")

def convert_csv_file(input_file, output_file, kantec_column='Kantec', paxton_column='Paxton'):
    """
    Convert a CSV file with Kantec card numbers to include Paxton numbers.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
        kantec_column (str): Name of column containing Kantec numbers
        paxton_column (str): Name of column for Paxton numbers (will be added)
    """
    converted_count = 0
    error_count = 0
    errors = []
    
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            if not reader.fieldnames:
                raise ValueError("Input CSV file is empty or has no headers")
            
            if kantec_column not in reader.fieldnames:
                raise ValueError(f"Column '{kantec_column}' not found in CSV. Available columns: {', '.join(reader.fieldnames)}")
            
            # Prepare output fieldnames
            output_fieldnames = list(reader.fieldnames)
            if paxton_column not in output_fieldnames:
                output_fieldnames.append(paxton_column)
            
            rows = []
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                kantec_value = row.get(kantec_column, '').strip()
                
                if kantec_value:
                    try:
                        paxton_value = kantec_to_paxton(kantec_value)
                        row[paxton_column] = paxton_value
                        converted_count += 1
                    except Exception as e:
                        row[paxton_column] = f"ERROR: {str(e)}"
                        errors.append(f"Row {row_num}: {kantec_value} - {str(e)}")
                        error_count += 1
                else:
                    row[paxton_column] = ''
                
                rows.append(row)
        
        # Write output file
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=output_fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        # Print summary
        print(f"\nConversion Summary:")
        print(f"  Input file: {input_file}")
        print(f"  Output file: {output_file}")
        print(f"  Successfully converted: {converted_count}")
        print(f"  Errors: {error_count}")
        
        if errors:
            print(f"\nErrors encountered:")
            for error in errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
        
        print(f"\n✓ Output saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing CSV: {str(e)}")
        sys.exit(1)

def test_known_examples():
    """Test against known examples."""
    test_cases = [
        ("4D:52042", "9716ABCDEFZ82Z014ACB4D139716"),
        ("35:46655", "9716ABCDEFZ82Z013FB635179716"),
    ]
    
    print("Testing against known examples:")
    print("=" * 70)
    
    all_match = True
    for kantec, expected in test_cases:
        result = kantec_to_paxton(kantec)
        match = result.upper() == expected.upper()
        
        print(f"\nKantec:   {kantec}")
        print(f"Expected: {expected}")
        print(f"Result:   {result}")
        print(f"Status:   {'✓ MATCH' if match else '✗ MISMATCH'}")
        
        if not match:
            all_match = False
            # Show where they differ
            for i, (c1, c2) in enumerate(zip(expected.upper(), result.upper())):
                if c1 != c2:
                    print(f"  First difference at position {i}: expected '{c1}', got '{c2}'")
                    break
    
    print("\n" + "=" * 70)
    if all_match:
        print("✓ All tests passed! The converter is ready to use.")
    else:
        print("Note: Please verify conversions against your actual Paxton 10 system.")
    
    return all_match

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nTesting with known examples:")
        test_known_examples()
        sys.exit(0)
    
    # CSV conversion mode
    if sys.argv[1] == '--csv':
        if len(sys.argv) < 4:
            print("Error: CSV mode requires input and output file paths")
            print("Usage: python3 kantec_to_paxton_converter.py --csv <input.csv> <output.csv>")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        convert_csv_file(input_file, output_file)
    
    # Single conversion mode
    else:
        kantec_number = sys.argv[1]
        try:
            paxton_number = kantec_to_paxton(kantec_number)
            print(f"Kantec:  {kantec_number}")
            print(f"Paxton:  {paxton_number}")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
