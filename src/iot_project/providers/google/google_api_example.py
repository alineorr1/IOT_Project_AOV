#Libraries
import pandas as pd
import requests


#%%


class Client(object):
    DEFAULT_BASE_URL = "https://airquality.googleapis.com"

    def __init__(self, key):
        self.session = requests.Session()
        self.key = key

    def request_post(self, url, params):
        request_url = self.compose_url(url)
        request_header = self.compose_header()
        request_body = params

        response = self.session.post(
            request_url,
            headers=request_header,
            json=request_body,
        )

        return self.get_body(response)

    def compose_url(self, path):
        return self.DEFAULT_BASE_URL + path + "?" + "key=" + self.key

    @staticmethod
    def get_body(response):
        body = response.json()

        if "error" in body:
            return body["error"]

        return body

    @staticmethod
    def compose_header():
        return {
            "Content-Type": "application/json",
        }


#%%

def current_conditions(
    client,
    location,
    include_local_AQI=True,
    include_health_suggestion=False,
    include_all_pollutants=True,
    include_additional_pollutant_info=False,
    include_dominent_pollutant_conc=True,
    language=None,
):
    """
    See documentation for this API here
    https://developers.google.com/maps/documentation/air-quality/reference/rest/v1/currentConditions/lookup
    """
    params = {}

    if isinstance(location, dict):
        params["location"] = location
    else:
        raise ValueError(
            "Location argument must be a dictionary containing latitude and longitude"
        )

    extra_computations = []
    if include_local_AQI:
        extra_computations.append("LOCAL_AQI")

    if include_health_suggestion:
        extra_computations.append("HEALTH_RECOMMENDATIONS")

    if include_additional_pollutant_info:
        extra_computations.append("POLLUTANT_ADDITIONAL_INFO")

    if include_all_pollutants:
        extra_computations.append("POLLUTANT_CONCENTRATION")

    if include_dominent_pollutant_conc:
        extra_computations.append("DOMINANT_POLLUTANT_CONCENTRATION")

    if language:
        params["language"] = language

    params["extraComputations"] = extra_computations

    return client.request_post("/v1/currentConditions:lookup", params)

#%%

def request_post(self,url,params):

  request_url = self.compose_url(url)
  request_header = self.compose_header()
  request_body = params

  response = self.session.post(
    request_url,
    headers=request_header,
    json=request_body,
  )

  response_body = self.get_body(response)

  # put the first page in the response dictionary
  page = 1
  final_response = {
      "page_{}".format(page) : response_body
  }
  # fetch all the pages if needed 
  while "nextPageToken" in response_body:
    # call again with the next page's token
    request_body.update({
        "pageToken":response_body["nextPageToken"]
    })
    response = self.session.post(
        request_url,
        headers=request_header,
        json=request_body,
    )
    response_body = self.get_body(response)
    page += 1
    final_response["page_{}".format(page)] = response_body

  return final_response

#%%

def historical_conditions(
    client,
    location,
    specific_time=None,
    lag_time=None,
    specific_period=None,
    include_local_AQI=True,
    include_health_suggestion=False,
    include_all_pollutants=True,
    include_additional_pollutant_info=False,
    include_dominant_pollutant_conc=True,
    language=None,
):
    """
    See documentation for this API here https://developers.google.com/maps/documentation/air-quality/reference/rest/v1/history/lookup
    """
    params = {}

    if isinstance(location, dict):
        params["location"] = location
    else:
        raise ValueError(
            "Location argument must be a dictionary containing latitude and longitude"
        )

    if isinstance(specific_period, dict) and not specific_time and not lag_time:
        assert "startTime" in specific_period
        assert "endTime" in specific_period

        params["period"] = specific_period

    elif specific_time and not lag_time and not isinstance(specific_period, dict):
        # note that time must be in the "Zulu" format
        # e.g. datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%dT%H:%M:%SZ")
        params["dateTime"] = specific_time

    # lag periods in hours
    elif lag_time and not specific_time and not isinstance(specific_period, dict):
        params["hours"] = lag_time

    else:
        raise ValueError(
            "Must provide specific_time, specific_period or lag_time arguments"
        )

    extra_computations = []
    if include_local_AQI:
        extra_computations.append("LOCAL_AQI")

    if include_health_suggestion:
        extra_computations.append("HEALTH_RECOMMENDATIONS")

    if include_additional_pollutant_info:
        extra_computations.append("POLLUTANT_ADDITIONAL_INFO")

    if include_all_pollutants:
        extra_computations.append("POLLUTANT_CONCENTRATION")

    if include_dominant_pollutant_conc:
        extra_computations.append("DOMINANT_POLLUTANT_CONCENTRATION")

    if language:
        params["language"] = language

    params["extraComputations"] = extra_computations
    # page size default set to 100 here
    params["pageSize"] = 200
    # page token will get filled in if needed by the request_post method
    params["pageToken"] = ""

    return client.request_post("/v1/history:lookup", params)


#%%

def historical_weather_data(api_key: str, location_dict: dict) -> pd.DataFrame:
    """
    Parameters
    ----------
    history_conditions_data : dict
        DESCRIPTION.

    Returns
    -------
    None.
    
    location = {"longitude": -99.1332, "latitude": 19.4326}
    # set up client
    client = Client(key=google_api)
    # a location in Los Angeles, CA
    # location = {"longitude":-118.3,"latitude":34.1}
    # a JSON response
    history_conditions_data = historical_conditions(
        client,
        location,
        lag_time=720
    )

    """
    
    # location = {"longitude": -99.1332, "latitude": 19.4326}
    # set up client
    client = Client(key=api_key)
    # a location in Los Angeles, CA
    # location = {"longitude":-118.3,"latitude":34.1}
    # a JSON response
    history_conditions_data = historical_conditions(
        client,
        location_dict,
        lag_time=720
    )

    hours_info_list = history_conditions_data.get("hoursInfo", [])
    
    data = []
    
    for entry in hours_info_list:
        date_time = entry["dateTime"]
        
        indexes_data = {}
        for i, index in enumerate(entry.get("indexes", []), start=1):
            indexes_data[f"index_{i}_aqi"] = index.get("aqi", None)
            indexes_data[f"index_{i}_category"] = index.get("category", None)
            if "color" in index and isinstance(index["color"], dict):
                indexes_data[f"index_{i}_color_red"] = index["color"].get("red", None)
                indexes_data[f"index_{i}_color_green"] = index["color"].get("green", None)
                indexes_data[f"index_{i}_color_blue"] = index["color"].get("blue", None)
        
        pollutants_data = {}
        for pollutant in entry.get("pollutants", []):
            pollutant_code = pollutant.get("code", "Unknown")
            pollutants_data[f"{pollutant_code}_concentration_value"] = pollutant.get("concentration", {}).get("value", None)
            pollutants_data[f"{pollutant_code}_concentration_units"] = pollutant.get("concentration", {}).get("units", None)
        
        combined_data = {"dateTime": date_time, **indexes_data, **pollutants_data}
        data.append(combined_data)
    
    df = pd.DataFrame(data)
    
    return df
    