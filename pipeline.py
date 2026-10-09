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
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report


logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
    level=level,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)

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

def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if not Path(filepath).is_file():
        logger.error(f"File not found: '{filepath}'")
        return False
    else:
        logger.info(f"File validated: '{filepath}'")
        return True

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
    
    original = data.copy()
    try:
        cleaned = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(original, cleaned)
    print(report)
    logger.info(f"Processing complete: {len(original)} → {len(cleaned)} rows")

    cleaned.to_csv(args.output, index=False)
    logger.info(f"Saved cleaned data to {args.output}")
if __name__ == "__main__":
    main()
