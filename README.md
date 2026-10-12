MP1 PIPELINE FUNCTIONALITY:

This pipeline works to take in a CSV file, validate it, clean it, and save the result as a new CSV file using the instruction from the YAML configuration. Each function and file has its own role and position in this pipeline process, the main one being pipeline.py which coordinates all the different steps and reads through the command line arguments. The "src/" holds the modules that connect to each step. Beginning with "utils.py" which sets up the logging and checks that the input and config file are readable. "src/" also contains "data_loaders.py" which reads the CSV file provided(in this case, the test file is located in "fixtures/") and YAML config. "data_validator.py" goes through required and numeric columns checking for invalid data. Then, "data_processor.py" removes these inconsistencies like outliers, missing values, and duplicates which in the end creates a cleaned report. Lastly, this newly cleaned data is saved to a new CSV file located in the output folder. 

# Example Test:

python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose

# Result:

14:16:14 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
14:16:14 INFO     src.utils — File validated: 'fixtures/sample_data.csv'
14:16:14 INFO     src.utils — File validated: 'config/config.yaml'
14:16:14 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv with 100 rows
14:16:14 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
14:16:14 WARNING  src.data_validator — Invalid numeric value on row: 94
14:16:14 WARNING  src.data_validator — Invalid numeric value on row: 95
14:16:14 DEBUG    src.data_validator — Cleaned dataframe: Had 98 valid rows and 2 invalid rows.
14:16:14 INFO     __main__ — Validated process: 100 -> 98 rows.
14:16:14 DEBUG    src.data_processor — Remove duplicates: 98 -> 96 rows
14:16:14 DEBUG    src.data_processor — Handle_missing: 96 → 94 rows
14:16:14 DEBUG    src.data_processor — Removed 2 rows using the iqr method with a 1.5 threshold. 
14:16:14 INFO     __main__ — Processing complete: 98 → 92 rows
14:16:14 DEBUG    src.data_output — 92 rows saved to output/clean.csv.
14:16:14 INFO     __main__ — Saved cleaned data to output/clean.csv
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}


