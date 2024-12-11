#Libraries
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.pyplot import figure
from matplotlib.dates import DateFormatter

#logging config
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Logger Config
logger = logging.getLogger('myAppLogger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')

#%%

#params
oura_data_path = 'Input/oura_data/oura_activities.json'

#%%

#functions
def data_wrangler_oura_json(file_path: str) -> dict:
    """
    Parameters
    ----------
    file_path : str
        path where data is located.

    Returns
    -------
    data : dict
        Oura data in json format.

    """
    with open(file_path) as activities_file:
        data = json.load(activities_file)
        return data

#%%

data = data_wrangler_oura_json(oura_data_path)

full_df = pd.DataFrame.from_dict(data['sleep'])

#%%

full_df['datetime'] = pd.to_datetime(full_df['bedtime_end'], utc=True).dt.normalize()
full_df['weekday'] = full_df['datetime'].dt.dayofweek
full_df['weekend'] = (full_df['datetime'].dt.dayofweek > 4).astype(int)
full_df['datetime_naive'] = full_df['datetime'].apply(lambda t: t.replace(tzinfo=None))
full_df = full_df.set_index('datetime_naive')
full_df.info()
full_df['weekend']

#%%

df = full_df.drop('is_longest', axis=1) 

# calculate some extra numerical statistics for fun correlations
df['bedtime_start_hour'] = pd.to_datetime(df['bedtime_start'], utc=True).dt.hour
df['bedtime_end_hour'] = pd.to_datetime(df['bedtime_end'], utc=True).dt.hour

#%%

# Here is the fast and easy way to plot correlations
# Here I need to drop non numerical columns

corr = df.corr()
corr.style.background_gradient(cmap='coolwarm')
corr.style.background_gradient(cmap='coolwarm').set_precision(2)

#%%

f = plt.figure(figsize=(28, 18))
plt.matshow(df.corr(), fignum=f.number)
plt.xticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14, rotation=90)
plt.yticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
plt.title('Correlation Matrix', fontsize=16);

#%%

corr = df.corr()['score'].sort_values()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    logger.info(corr)

#%%

df_next = df['score'] # Create another subset of data to compare
df_next = df_next.shift(periods=-1, axis=0, fill_value=0) # Shift back by one (compare days data with next days score)
df = df.join(df_next, rsuffix="_next") # Join to original df with a new name

#%%

# Here is the fast and easy way to plot correlations
corr = df.corr()
corr.style.background_gradient(cmap='coolwarm')
corr.style.background_gradient(cmap='coolwarm').set_precision(2)

#%%

full_activity_df = pd.DataFrame.from_dict(data['activity'])
# Index by summary_date aka day when activity period started, 4AM
full_activity_df['datetime'] = pd.to_datetime(full_activity_df['summary_date']).dt.normalize()
full_activity_df.head()
full_activity_df = full_activity_df.set_index('datetime')
full_activity_df.info()

#%%

df_next = df['score'] # Create another subset of data to compare
df_next = df_next.shift(periods=-1, axis=0, fill_value=0) # Shift back by one (compare days data with next days score)
full_activity_df = full_activity_df.join(df_next, lsuffix='_activity', rsuffix='_sleep') # Join to original df with a new name

# Cleanup the data a bit by dropping NaN and 0 values
full_activity_df = full_activity_df.dropna(subset=['score_sleep'])

full_activity_df.head()

#%%

corr = full_activity_df.corr()['score_sleep'].sort_values()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    logger.info(corr)

#%%






