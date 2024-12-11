#Personal Modules
from src.iot_project.providers.oura import oura_data_manipulation as odm

#Libraries
import pandas as pd

#logging config
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Logger Config
logger = logging.getLogger('myAppLogger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')

#%%

def complete_oura_df_obtaintion(api_key_oura: str) -> dict:
    """
    Parameters
    ----------
    api_key_oura : str
        api key from oura.

    Returns
    -------
    dict
        The final dict with two dfs.

    """
    final_info_dict = {}

    data_dict = odm.oura_complete_data_retrieving(api_key=api_key_oura)

    data_dict_df = odm.oura_data_to_df(data_dict=data_dict)
    
    personal_info = data_dict['personal_info']

    # Uso de la función
    dfs_to_merge = [
        data_dict_df['daily_activity_df'],
        data_dict_df['daily_cardiovascular_age_df'],
        data_dict_df['daily_readiness_df'],
        data_dict_df['daily_sleeps_df'],
        data_dict_df['daily_spo2_df'],
        data_dict_df['daily_stress_df']
    ]

    merged_df_final = odm.merge_multiple_dfs(dfs=dfs_to_merge)

    merged_df_final.fillna(method='ffill', inplace=True)

    merged_df_final = merged_df_final.set_index('day')

    merged_df_final = merged_df_final[~merged_df_final.index.duplicated(keep='last')]

    personal_info_df = pd.DataFrame([personal_info])
    
    final_info_dict['merged_df_final'] = merged_df_final
    
    final_info_dict['personal_info_df'] = personal_info_df

    return final_info_dict, data_dict_df