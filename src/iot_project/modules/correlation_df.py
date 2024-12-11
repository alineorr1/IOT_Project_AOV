#Libraries
import pandas as pd

#%%

def correlation_matrix(df_x: pd.DataFrame) -> pd.DataFrame():
    
    numerical_df = df_x.select_dtypes(include=['number'])
    numerical_df = numerical_df.drop(['interval', 'recovery_time'], axis=1)

    correlation_df = numerical_df.corr()
    correlation_df = correlation_df.round(2)

    return correlation_df
