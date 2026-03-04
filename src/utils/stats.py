import pandas as pd

def get_data_summary(df: pd.DataFrame):
    return {
        "total_rows": len(df),
        "total_cols": len(df.columns),
        "missing_values": df.isnull().sum().sum(),
        "numeric_cols": len(df.select_dtypes(include=['number']).columns)
    }