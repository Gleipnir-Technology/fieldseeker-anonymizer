#!/usr/bin/env python3
import csv
import argparse
import collections
import hashlib
import sys
import uuid

def anonymize_value(value):
	"""
	Anonymizes a string using SHA-256 hashing.
	"""
	if value is None:
		return ""
	# Encode the string to bytes, hash it, then convert back to a hex string
	return hashlib.sha256(value.encode('utf-8')).hexdigest()[:20]

def main():
	# 1. Setup Argument Parsing
	parser = argparse.ArgumentParser(
		description="Anonymize specific columns in a CSV file and print to stdout."
	)
	
	parser.add_argument(
		'input',
		nargs='+',
		help="Path to the source CSV file."
	)
	
	parser.add_argument(
		'-c', '--columns', 
		nargs='+', 
		required=True, 
		help="List of column names to anonymize (separated by space)."
	)

	parser.add_argument(
		'-s', '--set',
		nargs='+',
		required=False,
		help="Columns to set to a specific value"
	)
	args = parser.parse_args()

	print(f"Remapping {args.columns}")
	remapped_values = [s.split("=") for s in args.set]
	print(f"Setting {remapped_values}")

	new_globalids = collections.defaultdict(lambda:uuid.uuid4())
	for input_file in args.input:
		output_file = input_file.split(".")[0] + "-anonymized.csv"
		# 2. Open the input file
		print(f"Reading {input_file}")
		with open(input_file, mode='r', newline='', encoding='utf-8') as csvfile:
			reader = csv.DictReader(csvfile)
			
			# check if file is empty or has no header
			if not reader.fieldnames:
				sys.stderr.write("Error: CSV file appears to be empty or missing headers.\n")
				sys.exit(1)

			# 3. Validate that requested columns exist
			input_headers = reader.fieldnames

			# 4. Setup the Writer (Standard Output)
			with open(output_file, mode="w", encoding="utf-8") as outfile:
				writer = csv.DictWriter(outfile, fieldnames=input_headers)
				writer.writeheader()

				# 5. Process row by row
				for row in reader:
					new_globalid = new_globalids[row["globalid"]]
					row["globalid"] = new_globalid
					for col in args.columns:
						# Apply the hashing function to the specific columns
						#print(f"setting {col} to {anonymize_value(row[col])}")
						if col in row:
							row[col] = anonymize_value(row[col])
					
					for col, val in remapped_values:
						#print(f"pretending to set {col} to {val}")
						if col in row:
							row[col] = val
					writer.writerow(row)
				print(f"Wrote {output_file}")

if __name__ == "__main__":
	main()
