"""
pip3 install cloudscraper requests readchar pwinput

export EMAIL=<your garmin email>
export PASSWORD=<your garmin password>

"""

#Libraries
import datetime
import json
import logging
import os
import sys

import requests
import pwinput
import readchar

#logging config
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Logger Config
logger = logging.getLogger('myAppLogger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

#%%

email = 'lilianpintor97@gmail.com'
password = 'Triomaravilla2'

api = Garmin('lilianpintor97@gmail.com', 'Triomaravilla2')

# Example selections and settings
today = datetime.date.today()
startdate = today - datetime.timedelta(days=58) # Select past week
start = 0
limit = 100
start_badge = 1  # Badge related calls calls start counting at 1
activitytype = ""  # Possible values are: cycling, running, swimming, multi_sport, fitness_equipment, hiking, walking, other
activityfile = "MY_ACTIVITY.fit" # Supported file types are: .fit .gpx .tcx

#%%

def init_api():
    api = Garmin('lilianpintor97@gmail.com', 'Triomaravilla2')
    api.login()

    return api

api = init_api()

#%%

start_date = datetime.date(2023, 12, 1)
end_date = datetime.date(2024, 11, 30)

activities = api.get_activities_by_date(
                start_date.isoformat(), end_date.isoformat(), 'cycling')

for activity in activities:
    activity_id = activity["activityId"]
    gpx_data = api.download_activity(
                        activity_id, dl_fmt=api.ActivityDownloadFormat.GPX
                    )









