#Personal Modules
from src.iot_project.dashboard.dash_components.navigation import navbar
from src.iot_project.dashboard.general_functions import webrowser_opening as wo
from src.iot_project.providers.oura import oura_api as our
from src.iot_project.dashboard.app_callback import app_callback
from src.iot_project.dashboard.pages.callbacks.day_analysis_callbacks import register_callback_actuals
from src.iot_project.dashboard.pages.callbacks.historical_oura_analysis_callbacks import historical_oura_analysis_callback
from src.iot_project import open_ai_llm as summ
from src.iot_project.modules import dotenv_loader as doten
from src.iot_project.dashboard.pages.callbacks.heart_rate_callbacks import register_callbacks
from src.iot_project.dashboard.pages.callbacks.weather_quality_callbacks import register_weather_callbacks

# Libraries
from threading import Timer
# Dash
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd
import logging
#logging config
logger = logging.getLogger('myAppLogger')

#%%

doten.load_config_env()
oura = os.getenv('KNDC_API_KEY_OURA')
openai = os.getenv('KNDC_API_KEY_OPENAI')
google = os.getenv('KNDC_API_KEY_GOOGLE')

data_dict, general_data_dict = our.complete_oura_df_obtaintion(api_key_oura=oura)

#%%

merged_df_final = data_dict['merged_df_final']
personal_info_df = data_dict['personal_info_df']
heart_rate_df = general_data_dict['heartrate_df']

heart_rate_df["timestamp"] = pd.to_datetime(heart_rate_df["timestamp"])
heart_rate_df.set_index("timestamp", inplace=True)

hourly_df = heart_rate_df.resample("H").agg({
    "bpm": "mean",
    "source": lambda x: x.mode()[0] if not x.empty else None
})

# hourly_df = hourly_df.reset_index()

hourly_df = hourly_df.reset_index()

hourly_df["bpm"] = hourly_df["bpm"].round(2)


#%%

merged_df_final_2 = merged_df_final.reset_index()


#%%

json_text = merged_df_final.to_json(orient='records', lines=False, indent=4)

#%%

logger.info("Loading your personal recommendation from GPT-4-mini")
final_summary = summ.chat_gpt_summary(api_key=openai, input_text=json_text)

#%%

app = dash.Dash(__name__, suppress_callback_exceptions=True, 
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,  
    html.Div(id='page-content'),
    html.Footer(
        html.Div(
            [
                html.Hr(),
                dcc.Markdown(
                """
                **Health Monitor**  
                """
                ),
                html.P(
                    [
                        html.Img(src=dash.get_asset_url("iot.png")),
                        html.Span("   "),
                        html.A("GitHub Repository", href="https://github.com/Sebastian-KaxaNuk/IOT_Project", target="_blank"),
                    ]
                ),
            ],
            style={"text-align": "center"},
            className="p-3",
        ),
    )
])

#===========================================================================================
#                                           APP CALLBACK
#===========================================================================================

app_callback(app, complete_oura_df=merged_df_final)

register_callback_actuals(app, 
                          complete_oura_ring_df=merged_df_final, 
                          personal_info_oura=personal_info_df,
                          text=final_summary)

#===========================================================================================
#                                           HISTORICAL
#===========================================================================================

historical_oura_analysis_callback(app, 
                                  complete_oura_ring_df=merged_df_final_2)

#===========================================================================================
#                                           HISTORICAL
#===========================================================================================

register_callbacks(app, heart_rate_df=hourly_df)

#===========================================================================================
#                                           HISTORICAL
#===========================================================================================

register_weather_callbacks(app, api_key=google)


if __name__ == "__main__":
    logger.info('-----------------------------------------')
    logger.info("Dash is running on http://127.0.0.1:8031/")
    logger.info('-----------------------------------------')
    Timer(1, wo.open_browser).start();
    app.run_server(debug=False, port=8031)
