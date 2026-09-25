from pathlib import Path

import logging
import pandas as pd
import json
import yaml


# Do not call logging.basicConfig() here.
# Use the logging configuration from Part 1.
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load a CSV file into a DataFrame.
    filepath is a Path object.
    """
    df = pd.read_csv(filepath)
    logger.info(f"Loaded CSV file: {filepath} with {len(df)} rows")
    return df

def load_json(filepath):
    """Load a JSON file into a Python object (dict or list).
    filepath is a Path object.
    """
    with open(filepath, "r") as f:
        info = json.load(f)
    logger.info(f"Loaded JSON file: {filepath}")
    return info


def load_yaml(filepath):
    """Load a YAML file into a Python object.
    filepath is a Path object.
    """
    with open(filepath, "r") as f:
        info = yaml.safe_load(f)
    logger.info(f"Loaded YAML file: {filepath}")


def load_data(filepath):
    """Load a file based on its extension.
    filepath is a string, such as 'fixtures/sample.csv'
    """
    path = Path(filepath)
    extension = path.suffix

    loaders = {
        ".csv": load_csv,
        ".json": load_json,
        ".yaml": load_yaml
    }

    loader = loaders.get(extension)
    if loader is None:
        logger.error(f"Unsupported file: {extension}")
        raise ValueError(f"Unsupported file: {extension}")
    return loader(path)
