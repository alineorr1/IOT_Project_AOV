#Libraries
import pandas as pd

#%%

def filter_day_columns(df: pd.DataFrame, 
                       day: str, 
                       columns: list[str]) -> pd.DataFrame:
    """
    Filters a DataFrame by a specific day and selects specific columns.

    Args:
        df (pd.DataFrame): Original DataFrame with days as the index.
        day (str): Specific day to filter (format must match the DataFrame index).
        columns (list): List of columns to select.

    Returns:
        pd.DataFrame: Filtered DataFrame with the specified day and selected columns.
    """
    if day not in df.index:
        raise ValueError(f"The day '{day}' is not present in the DataFrame index.")
    
    available_columns = [col for col in columns if col in df.columns]
    if not available_columns:
        raise ValueError("None of the specified columns are present in the DataFrame.")
    
    return df.loc[[day], available_columns]