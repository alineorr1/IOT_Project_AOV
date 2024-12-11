# Libraries
import pandas as pd

#%%

def calculate_intense_activity_ratio_from_df(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the ratio of high-intensity activity time to total active time for each row in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'high_activity_time', 'low_activity_time', 
                           and 'medium_activity_time'.

    Returns:
        pd.Series: A Series containing the ratio of high-intensity activity time to total active time.
    """
    total_activity_time = df['high_activity_time'] + df['low_activity_time'] + df['medium_activity_time']
    return df['high_activity_time'] / total_activity_time.replace(0, float('nan'))

def calculate_calorie_efficiency_from_df(df: pd.DataFrame) -> pd.Series:
    """
    Calculate calorie efficiency (calories burned per step) for each row in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'active_calories' and 'steps'.

    Returns:
        pd.Series: A Series containing calories burned per step.
    """
    return df['active_calories'] / df['steps'].replace(0, float('nan'))


def calculate_calorie_target_percentage_from_df(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the percentage of calorie target achieved for each row in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'active_calories' and 'target_calories'.

    Returns:
        pd.Series: A Series containing the percentage of calorie target achieved.
    """
    return (df['active_calories'] / df['target_calories'].replace(0, float('nan'))) * 100

def calculate_activity_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate additional activity metrics and ratios.

    Args:
        df (pd.DataFrame): DataFrame containing daily activity data with specific columns.

    Returns:
        pd.DataFrame: Updated DataFrame with new calculated ratios.
    """
    df = df.copy()
    
    # Active time percentage
    df['active_time_percentage'] = (
        (df['low_activity_time'] + df['medium_activity_time'] + df['high_activity_time']) /
        (1440 - df['non_wear_time'])
    ) * 100

    # Sedentary time percentage
    df['sedentary_time_percentage'] = (df['sedentary_time'] / (1440 - df['non_wear_time'])) * 100

    # Average intensity
    df['average_intensity'] = (
        (df['low_activity_met_minutes'] + df['medium_activity_met_minutes'] + df['high_activity_met_minutes']) /
        (df['low_activity_time'] + df['medium_activity_time'] + df['high_activity_time']).replace(0, float('nan'))
    )

    # Distance per step
    df['distance_per_step'] = (
        df['equivalent_walking_distance'] / df['steps'].replace(0, float('nan'))
    )

    # Recovery to high activity ratio
    df['recovery_to_high_activity_ratio'] = (
        df['recovery_time'] / df['high_activity_time'].replace(0, float('nan'))
    )

    # Inactivity alert ratio
    df['inactivity_alert_ratio'] = (
        df['inactivity_alerts'] / df['sedentary_time'].replace(0, float('nan'))
    )

    # Calories target percentage
    df['calories_target_percentage'] = (
        (df['active_calories'] / df['target_calories'].replace(0, float('nan'))) * 100
    )

    # Distance target percentage
    df['distance_target_percentage'] = (
        (df['equivalent_walking_distance'] / df['target_meters'].replace(0, float('nan'))) * 100
    )

    # Training effectiveness
    df['training_effectiveness'] = (
        df['training_volume'] / df['training_frequency'].replace(0, float('nan'))
    )

    return df

def calculate_vascular_related_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate additional metrics related to vascular age and activity.

    Args:
        df (pd.DataFrame): Merged DataFrame containing vascular age and activity data.

    Returns:
        pd.DataFrame: DataFrame with additional calculated metrics.
    """
    df = df.copy()
    
    # Active to vascular ratio
    df['active_to_vascular_ratio'] = df['active_time_percentage'] / df['vascular_age']
    
    # Training to vascular ratio
    df['training_to_vascular_ratio'] = df['training_effectiveness'] / df['vascular_age']
    
    # Sedentary to vascular ratio
    df['sedentary_to_vascular_ratio'] = df['sedentary_time'] / df['vascular_age']
    
    # Average calories by vascular age range
    bins = [0, 50, 55, 60, 100]  # Example age ranges
    labels = ['<50', '50-55', '55-60', '>60']
    df['vascular_age_range'] = pd.cut(df['vascular_age'], bins=bins, labels=labels)
    df['avg_calories_by_vascular_age'] = df.groupby('vascular_age_range')['active_calories'].transform('mean')
    # Calories to vascular ratio
    df['calories_to_vascular_ratio'] = df['active_calories'] / df['vascular_age']
    
    # Sedentary impact
    df['sedentary_impact'] = df['sedentary_time'] / df['vascular_age']
    
    # Adjusted calorie efficiency
    df['adjusted_calorie_efficiency'] = df['calorie_efficiency'] / df['vascular_age']
    
    # Steps to vascular ratio
    df['steps_to_vascular_ratio'] = df['steps'] / df['vascular_age']
    
    # Active time to vascular
    df['active_time_to_vascular'] = df['active_time_percentage'] / df['vascular_age']
    return df

def calculate_readiness_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate metrics exclusive to daily_readiness_df.

    Args:
        df (pd.DataFrame): DataFrame containing readiness metrics.

    Returns:
        pd.DataFrame: Updated DataFrame with calculated readiness metrics.
    """
    df = df.copy()
    
    # Combined temperature deviation
    df['combined_temp_deviation'] = df['temperature_deviation'] + df['temperature_trend_deviation']
    
    # Recovery index to activity balance ratio
    df['recovery_to_activity_ratio'] = df['recovery_index'] / df['activity_balance']
    
    # Rolling readiness score (7-day moving average)
    df['rolling_readiness_score'] = df['score'].rolling(window=7).mean()
    
    # Sleep balance to recovery ratio
    df['sleep_to_recovery_ratio'] = df['sleep_balance'] / df['recovery_index']
    
    # Resting heart rate to activity balance ratio
    df['rhr_to_activity_ratio'] = df['resting_heart_rate'] / df['activity_balance']
    
    return df

def calculate_readiness_combined_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate combined metrics after merging readiness, activity, and vascular data.

    Args:
        df (pd.DataFrame): Merged DataFrame containing readiness, activity, and vascular metrics.

    Returns:
        pd.DataFrame: Updated DataFrame with new combined metrics.
    """
    df = df.copy()
    
    # Temperature to vascular impact
    df['temp_to_vascular_impact'] = df['combined_temp_deviation'] / df['vascular_age']
    
    # Readiness to vascular ratio
    df['readiness_to_vascular_ratio'] = df['score_x'] / df['vascular_age']
    
    # Resting heart rate to vascular ratio
    df['rhr_to_vascular_ratio'] = df['resting_heart_rate'] / df['vascular_age']
    
    # Recovery to vascular ratio
    df['recovery_to_vascular_ratio'] = df['recovery_index'] / df['vascular_age']
    
    # Activity balance to vascular ratio
    df['activity_balance_to_vascular'] = df['activity_balance'] / df['vascular_age']
    
    return df

def calculate_sleep_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate additional sleep metrics for daily_sleep_df.

    Args:
        df (pd.DataFrame): DataFrame containing sleep data.

    Returns:
        pd.DataFrame: Updated DataFrame with calculated sleep metrics.
    """
    df = df.copy()
    
    # Deep sleep percentage
    df['deep_sleep_percentage'] = (df['deep_sleep'] / df['total_sleep']) * 100
    
    # REM sleep percentage
    df['rem_sleep_percentage'] = (df['rem_sleep'] / df['total_sleep']) * 100
    
    # Rest efficiency index
    df['rest_efficiency_index'] = df['restfulness'] * df['efficiency']
    
    # Latency to timing ratio
    df['latency_to_timing_ratio'] = df['latency'] / df['timing']
    
    # Deep to REM ratio
    df['deep_to_rem_ratio'] = df['deep_sleep'] / df['rem_sleep']
    
    # Rolling sleep score
    df['rolling_sleep_score'] = df['score'].rolling(window=7).mean()
    
    return df