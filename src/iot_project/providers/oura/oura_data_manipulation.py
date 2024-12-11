#Personal Modules
from src.iot_project.providers.oura import oura_ring_provider as orp

#Libraries
import pandas as pd
from datetime import datetime
import time
from datetime import timedelta
#logging config
import logging
logger = logging.getLogger('myAppLogger')

#%%

def merge_dfs(
    df1: pd.DataFrame, 
    df2: pd.DataFrame, 
    date_column: str = 'day'
) -> pd.DataFrame:
    """
    Merge the daily activity and cardiovascular age DataFrames on a common date column.

    Args:
        activity_df (pd.DataFrame): DataFrame containing daily activity data.
        cardiovascular_df (pd.DataFrame): DataFrame containing daily cardiovascular age data.
        date_column (str): Name of the column to merge on (default is 'day').

    Returns:
        pd.DataFrame: A merged DataFrame.
    """
    df1[date_column] = pd.to_datetime(df1[date_column])
    df2[date_column] = pd.to_datetime(df2[date_column])
    merged_df = pd.merge(df1, df2, on=date_column, how='left')
    return merged_df

def oura_complete_data_retrieving(api_key: str) -> dict:
    """
    Parameters
    ----------
    api_key : str
        API key for Oura API.

    Returns
    -------
    data_dict : dict
        Dictionary containing data retrieved from the Oura API.
    """    
    data_dict = {}
    
    client = orp.OuraAPIClient(api_key=api_key)
    
    today = datetime.now()

    start_date = today - timedelta(weeks=10)
    start_date_heart = today - timedelta(days=30)

    today_str = today.strftime('%Y-%m-%d')
    start_date_str = start_date.strftime('%Y-%m-%d')
    start_date_heart = start_date_heart.strftime('%Y-%m-%d')

    start_datetime_heart =  start_date_heart + 'T00:00:00-08:00' 
    end_datetime_heart = today_str + 'T00:00:00-08:00' 
    
    # Helper function to extract 'data' key
    def extract_data(api_response):
        return api_response.get('data', None)

    # Retrieving data and adding to the dictionary
    data_dict['daily_activity'] = extract_data(client.get_daily_activity(start_date=start_date_str, end_date=today_str))
    time.sleep(.02)

    data_dict['daily_cardiovascular_age'] = extract_data(client.get_daily_cardiovascular_age(start_date=start_date_str, end_date=today_str))
    time.sleep(.02)

    data_dict['daily_readiness'] = extract_data(client.get_daily_readiness(start_date=start_date_str, end_date=today_str))
    time.sleep(.02)

    data_dict['daily_sleeps'] = extract_data(client.get_daily_sleep(start_date=start_date_str, end_date=today_str))
    time.sleep(.02)

    data_dict['daily_stress'] = extract_data(client.get_daily_stress(start_date=start_date_str, end_date=today_str))
    time.sleep(.02)

    data_dict['daily_spo2'] = extract_data(client.get_daily_spo2(start_date=start_date_str, end_date=today_str))
    time.sleep(.02)

    data_dict['workouts'] = extract_data(client.get_workouts(start_date=start_date_str, end_date=today_str))
    time.sleep(.02)

    data_dict['heartrate'] = extract_data(client.get_heartrate(start_date=start_datetime_heart, end_date=end_datetime_heart))
    time.sleep(.02)

    # 'personal_info' is stored as-is
    data_dict['personal_info'] = client.get_personal_info(start_date=start_date_str, end_date=today_str)    

    return data_dict

def oura_data_to_df(data_dict: dict) -> dict[str, pd.DataFrame]:
    """
    Parameters
    ----------
    data_dict : dict
        Dictionary containing data retrieved from Oura API.

    Returns
    -------
    data_dict_df : dict[str, pd.DataFrame]
        Dictionary containing processed DataFrames from Oura API data.
    """    

    drop = ['id']
    data_dict_df = {}
    
    # Helper function to safely create DataFrames
    def safe_create_df(data, name):
        if data:  # Check if data is not None or empty
            try:
                return pd.DataFrame(data)
            except Exception as e:
                logger.error(f"Error processing {name}: {e}")
                return pd.DataFrame()
        else:
            logger.error(f"No data found for {name}.")
            return pd.DataFrame()

    # Process each dataset with safeguards
    try:
        daily_activity_df = safe_create_df(data_dict.get('daily_activity'), 'daily_activity')
        if not daily_activity_df.empty:
            daily_activity_df = daily_activity_df.rename(columns={'score': 'score_daily_activity'})
            contributors_df = pd.json_normalize(daily_activity_df['contributors'])
            met_df = pd.json_normalize(daily_activity_df['met'])
            daily_activity_df = pd.concat([daily_activity_df.drop(columns=['contributors']), 
                                           contributors_df,
                                           met_df], axis=1)
            daily_activity_df.drop(['id', 'met', 'class_5_min', 'items'], axis=1, inplace=True, errors='ignore')
            daily_activity_df.drop('timestamp', axis=1, inplace=True, errors='ignore')
            data_dict_df['daily_activity_df'] = daily_activity_df
    except Exception as e:
        logger.error(f"Error processing daily_activity: {e}")

    try:
        daily_cardiovascular_age_df = safe_create_df(data_dict.get('daily_cardiovascular_age'), 'daily_cardiovascular_age')
        if not daily_cardiovascular_age_df.empty:
            daily_cardiovascular_age_df = daily_cardiovascular_age_df.rename(columns={'score': 'score_daily_cardio_age'})
            data_dict_df['daily_cardiovascular_age_df'] = daily_cardiovascular_age_df
    except Exception as e:
        logger.error(f"Error processing daily_cardiovascular_age: {e}")

    try:
        daily_readiness_df = safe_create_df(data_dict.get('daily_readiness'), 'daily_readiness')
        if not daily_readiness_df.empty:
            contributors_df_readiness = pd.json_normalize(daily_readiness_df['contributors'])
            daily_readiness_df = pd.concat([daily_readiness_df.drop(columns=['contributors']), 
                                            contributors_df_readiness], axis=1)
            daily_readiness_df = daily_readiness_df.rename(columns={'score': 'score_daily_readiness'})
            daily_readiness_df.drop('timestamp', axis=1, inplace=True, errors='ignore')
            daily_readiness_df.drop(drop, axis=1, inplace=True, errors='ignore')
            data_dict_df['daily_readiness_df'] = daily_readiness_df
    except Exception as e:
        logger.error(f"Error processing daily_readiness: {e}")

    try:
        daily_sleeps_df = safe_create_df(data_dict.get('daily_sleeps'), 'daily_sleeps')
        if not daily_sleeps_df.empty:
            contributors_df_sleeps = pd.json_normalize(daily_sleeps_df['contributors'])
            daily_sleeps_df = pd.concat([daily_sleeps_df.drop(columns=['contributors']), 
                                         contributors_df_sleeps], axis=1)
            daily_sleeps_df = daily_sleeps_df.rename(columns={'score': 'score_daily_sleep'})
            daily_sleeps_df.drop('timestamp', axis=1, inplace=True, errors='ignore')
            daily_sleeps_df.drop(drop, axis=1, inplace=True, errors='ignore')
            data_dict_df['daily_sleeps_df'] = daily_sleeps_df
    except Exception as e:
        logger.error(f"Error processing daily_sleeps: {e}")

    try:
        daily_spo2_df = safe_create_df(data_dict.get('daily_spo2'), 'daily_spo2')
        if not daily_spo2_df.empty:
            spo2_percentage_df = pd.json_normalize(daily_spo2_df['spo2_percentage'])
            daily_spo2_df = pd.concat([daily_spo2_df.drop(columns=['spo2_percentage']), 
                                       spo2_percentage_df], axis=1)
            daily_spo2_df.drop(drop, axis=1, inplace=True, errors='ignore')
            data_dict_df['daily_spo2_df'] = daily_spo2_df
    except Exception as e:
        logger.error(f"Error processing daily_spo2: {e}")

    try:
        daily_stress_df = safe_create_df(data_dict.get('daily_stress'), 'daily_stress')
        if not daily_stress_df.empty:
            daily_stress_df.drop(drop, axis=1, inplace=True, errors='ignore')
            data_dict_df['daily_stress_df'] = daily_stress_df
    except Exception as e:
        logger.error(f"Error processing daily_stress: {e}")

    try:
        workouts_df = safe_create_df(data_dict.get('workouts'), 'workouts')
        data_dict_df['workouts_df'] = workouts_df
    except Exception as e:
        logger.error(f"Error processing workouts: {e}")

    try:
        heartrate_df = safe_create_df(data_dict.get('heartrate'), 'heartrate')
        data_dict_df['heartrate_df'] = heartrate_df
    except Exception as e:
        logger.error(f"Error processing heartrate: {e}")

    try:
        personal_id = data_dict.get('personal_info', {})
        data_dict_df['personal_id'] = personal_id
    except Exception as e:
        logger.error(f"Error processing personal_info: {e}")

    return data_dict_df

def merge_multiple_dfs(dfs: list[pd.DataFrame], date_column: str = 'day') -> pd.DataFrame:
    """
    Merge multiple DataFrames on a common date column.

    Args:
        dfs (list[pd.DataFrame]): List of DataFrames to merge.
        date_column (str): Name of the column to merge on (default is 'day').

    Returns:
        pd.DataFrame: A merged DataFrame.
    """
    if not dfs:
        return pd.DataFrame()  # Return an empty DataFrame if no DataFrames provided
    
    # Start with the first DataFrame
    merged_df = dfs[0].copy()
    
    # Merge iteratively with the remaining DataFrames
    for df in dfs[1:]:
        merged_df = merge_dfs(df1=merged_df, df2=df, date_column=date_column)
    
    return merged_df