#Libraries
import pandas as pd

#%%

def get_column_types(df: pd.DataFrame) -> dict[str, list[str]]:
    """
    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    column_types : dict[str, list[str]]
        Dictionary where keys are column types (numerical, categorical, object, etc.)
        and values are lists of column names for each type.
    """
    column_types = {
        "numerical": df.select_dtypes(include=['number']).columns.tolist(),
        "categorical": df.select_dtypes(include=['category']).columns.tolist(),
        "object": df.select_dtypes(include=['object']).columns.tolist(),
        "boolean": df.select_dtypes(include=['bool']).columns.tolist(),
        "datetime": df.select_dtypes(include=['datetime']).columns.tolist(),
        "other": df.select_dtypes(exclude=['number', 'category', 'object', 'bool', 'datetime']).columns.tolist()
    }
    
    return {key: value for key, value in column_types.items() if value}
