import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    og_rows = len(df)
    result = df.drop_duplicates()
    rows_dropped = og_rows - len(result)
    logger.debug(f"Remove duplicates: {og_rows} -> {len(result)} rows")
    return result

def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        og_rows = len(df)
        result = df.dropna(axis=0)
        logger.debug(f"Handle_missing: {og_rows} → {len(result)} rows")
    elif axis == "columns":
        og_columns = len(df.columns)
        result = df.dropna(axis=1)
        logger.debug(f"Handle_missing: {og_columns} → {len(result.columns)} columns")
    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")
    return result

def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ("iqr", "zscore"):
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")
    for col in columns:
        if col not in df.columns:
            logger.warning(f"Column not found: {col}")
            continue
        if col not in df.select_dtypes("number"):
            logger.warning(f"Column is not numeric: {col}")
            continue
        if method == "iqr":
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
        else:
            mean = df[col].mean()
            std = df[col].std()
            lower = mean - threshold * std
            upper = mean + threshold * std
            outlier = zscore.abs() > threshold

        outlier = (df[col] < lower) | (df[col] > upper)
        df = df[~outlier]
        logger.debug(f"Removed {outlier.sum()} rows using the {method} method with a {threshold} threshold. ")
    return df

def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    processing = config["processing"]
    if processing["remove_duplicates"]:
        df = remove_duplicates(df)
    
    missing = processing["missing"]
    if missing["enabled"]:
        df = handle_missing(df, axis=missing["axis"])

    outliers = processing["outliers"] 
    if outliers["enabled"]:
        df = remove_outliers(df, columns=outliers["columns"], method=outliers["method"], threshold=outliers["threshold"])
    return df

def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": len(df_before.columns) - len(df_after.columns)
    }