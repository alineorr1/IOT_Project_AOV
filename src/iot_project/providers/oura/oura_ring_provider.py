import json
import types
import urllib.error
import urllib.parse
import urllib.request
# import os
import requests

#logging config
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Logger Config
logger = logging.getLogger('myAppLogger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')

#Google
# from google.oauth2 import service_account

#%%

def heartrate_function(start_date: str, end_date: str, api_key: str) -> dict:
    """
    Parameters
    ----------
    start_date : str
        initial date.
    end_date : str
        final date.
    api_key : str
        oura ring api key.

    Returns
    -------
    dict
        data in json.

    'start_datetime': '2024-11-10T00:00:00-08:00', 
    'end_datetime': '2024-12-02T00:00:00-08:00' 
    """

    url = 'https://api.ouraring.com/v2/usercollection/heartrate' 
    params={ 
        'start_datetime': start_date, 
        'end_datetime': end_date 
    } 
    headers = { 
      'Authorization': f'Bearer {api_key}' 
    }
    response = requests.request('GET', url, headers=headers, params=params) 
    json = response.json()

    return json

#%%

class OuraAPIClient:
    """
    Client to interact with the Oura Ring API.
    """
    
    _endpoints = types.MappingProxyType({
        'Multiple_daily_activity_Documents': 'https://api.ouraring.com/v2/usercollection/daily_activity',
        'Multiple_daily_cardiovascular_age': 'https://api.ouraring.com/v2/usercollection/daily_cardiovascular_age',
        'Multiple_daily_readiness_Documents': 'https://api.ouraring.com/v2/usercollection/daily_readiness',
        'Multiple_daily_resilience_Documents': 'https://api.ouraring.com/v2/usercollection/daily_resilience',
        'Multiple_daily_sleep_Documents': 'https://api.ouraring.com/v2/usercollection/daily_sleep',
        'Daily-Spo2-Routes': 'https://api.ouraring.com/v2/usercollection/daily_spo2',
        'Daily-Stress-Routes': 'https://api.ouraring.com/v2/usercollection/daily_stress',
        'Multiple_enhanced_tag_Documents': 'https://api.ouraring.com/v2/usercollection/enhanced_tag',
        'Heart-Rate-Routes': 'https://api.ouraring.com/v2/usercollection/heartrate',
        'Multiple_rest_mode_period_Documents': 'https://api.ouraring.com/v2/usercollection/rest_mode_period',
        'Multiple_session_Documents': 'https://api.ouraring.com/v2/usercollection/session',
        'Multiple_sleep_Documents': 'https://api.ouraring.com/v2/usercollection/sleep',
        'Multiple_sleep_time_Documents': 'https://api.ouraring.com/v2/usercollection/sleep_time',
        'Multiple_vO2_max_Documents': 'https://api.ouraring.com/v2/usercollection/vO2_max',
        'Multiple_workout_Documents': 'https://api.ouraring.com/v2/usercollection/workout',
        'Personal_Info': 'https://api.ouraring.com/v2/usercollection/personal_info',
    })

    def __init__(self, api_key: str):
        """
        Initialize the client with an API key.

        Parameters
        ----------
        api_key : str
            The API key for authenticating requests.
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def url_builder(endpoint_url: str, params: dict) -> str:
        """
        Build the URL with query parameters.

        Parameters
        ----------
        endpoint_url : str
            The base URL of the endpoint.
        params : dict
            The parameters to add to the URL.

        Returns
        -------
        str
            The URL with the query parameters appended.
        """
        query_string = urllib.parse.urlencode(params)
        url = f"{endpoint_url}?{query_string}"
        return url

    def _request_data(self, endpoint_id: str, params: dict) -> str | None:
        """
        Perform a request to the specified endpoint.

        Parameters
        ----------
        endpoint_id : str
            The internal name of the endpoint, for logging purposes.
        params : dict
            The parameters to send in the request.

        Returns
        -------
        str or None
            The data in JSON format or None in case of an error.
        """
        endpoint_url = self._endpoints.get(endpoint_id)
        if not endpoint_url:
            logger.error(f"Endpoint ID '{endpoint_id}' not found.")
            return None

        url = self.url_builder(endpoint_url, params)
        http_request = urllib.request.Request(url, headers=self.headers)

        try:
            with urllib.request.urlopen(http_request) as response:
                content = response.read().decode('utf-8')
                logger.info(f"Data received from endpoint '{endpoint_id}': {content}")
                return json.loads(content)
        except urllib.error.URLError as e:
            logger.error(f"Error connecting to endpoint '{endpoint_id}': {e}")
            return None

    def get_data(self, endpoint_id: str, start_date: str, end_date: str) -> str | None:
        """
        Request data from an endpoint within a date range.

        Parameters
        ----------
        endpoint_id : str
            The ID of the endpoint to query.
        start_date : str
            The start date in 'YYYY-MM-DD' format.
        end_date : str
            The end date in 'YYYY-MM-DD' format.

        Returns
        -------
        str or None
            The data in JSON format or None in case of an error.
        """
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        return self._request_data(endpoint_id, params)

    # Specific methods for each endpoint
    def get_daily_activity(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Multiple_daily_activity_Documents', start_date, end_date)

    def get_daily_cardiovascular_age(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Multiple_daily_cardiovascular_age', start_date, end_date)

    def get_daily_readiness(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Multiple_daily_readiness_Documents', start_date, end_date)

    def get_daily_resilience(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Multiple_daily_resilience_Documents', start_date, end_date)

    def get_daily_sleep(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Multiple_daily_sleep_Documents', start_date, end_date)

    def get_daily_spo2(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Daily-Spo2-Routes', start_date, end_date)

    def get_daily_stress(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Daily-Stress-Routes', start_date, end_date)

    def get_enhanced_tags(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Multiple_enhanced_tag_Documents', start_date, end_date)
    
    def get_personal_info(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Personal_Info', start_date, end_date)

    def get_heartrate(self, start_date: str, end_date: str) -> dict | None:
        """
        Method that calls the external `heartrate` function.
    
        Parameters
        ----------
        start_date : str
            The initial date for the request.
        end_date : str
            The final date for the request.
    
        Returns
        -------
        dict or None
            The response JSON as a dictionary, or None in case of an error.
        """
        try:
            # Call the external heartrate function
            return heartrate_function(start_date=start_date, end_date=end_date, api_key=self.api_key)
        except Exception as e:
            logger.error(f"Error fetching heartrate data: {e}")
        return None

    def get_workouts(self, start_date: str, end_date: str) -> str | None:
        return self.get_data('Multiple_workout_Documents', start_date, end_date)
    
#%%

# df = pd.read_excel('Output/oura_data/oura_test.xlsx')

#%%

# df.to_gbq(project_id='iot-project-443517',
#           destination_table='Oura_dataset.daily_activity',
#           credentials=service_account.Credentials.from_service_account_file(
#               'iot-project-443517-fe13866b0cf2.json'),
#           progress_bar=True,
#           if_exists='append')

    
    