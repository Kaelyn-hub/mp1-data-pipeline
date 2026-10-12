'''
Data Processing Pipeline - CLI Template
DS 3500 - MP1

Usage:
python pipeline.py --input data.csv --output clean.csv
python pipeline.py --input data.csv --output results.json --format json --
verbose
'''
import argparse
import logging
import sys
from pathlib import Path

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Analyze a data file")
    parser.add_argument("--input",
                    "-i",
                    required=True,
                    help="Path to input file")   
    parser.add_argument("--output",
                    "-o",
                    required=True,
                    help="Path to output file")
    parser.add_argument("--config",
                        required=True,
                        help="Path to YAML configuration file")
    parser.add_argument("--verbose",
                    "-v",
                    action="store_true",
                    help="Enable verbose logging")
    args = parser.parse_args()
    return args

def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(f"Arguments parsed: input={args.input}, config={args.config}, output={args.output}")
    
    is_valid = validate_input(args.input)
    if not is_valid:
        sys.exit(1)
    is_config_valid = validate_input(args.config)
    if not is_config_valid:
        sys.exit(1)
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)
    
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    rows_before_validation = len(data)
    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(f"Validated process: {rows_before_validation} -> {len(data)} rows.")

    original = data.copy()
    try:
        cleaned = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(original, cleaned)
    logger.info(f"Processing complete: {len(original)} → {len(cleaned)} rows")

    output_path = save_data(cleaned, args.output)
    logger.info(f"Saved cleaned data to {output_path}")
    print(report)

if __name__ == "__main__":
    main()
