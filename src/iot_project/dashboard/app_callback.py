#Personal Modules
from src.iot_project.dashboard.pages.layouts import day_analysis_oura_layout as ol
from src.iot_project.dashboard.pages.layouts import historical_oura_analysis_layout as hl
from src.iot_project.dashboard.pages.layouts import heart_rate_layout as hr
from src.iot_project.dashboard.pages.layouts import weather_quality_layout as wq
# Libraries
from dash.dependencies import Input, Output
import pandas as pd

#%%

def app_callback(app, complete_oura_df: pd.DataFrame):
    
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    
    def display_page(pathname):
        if pathname == '/day-analysis':
            return ol.actuals_oura_ring(complete_oura_df=complete_oura_df)
        elif pathname == '/historical-page':
            return hl.historical_oura(complete_oura_ring_df=complete_oura_df)
        elif pathname == '/heartrate-page':
            return hr.heart_rate_layout()
        elif pathname == '/weather-page':
            return wq.weather_layout()
        # elif pathname == '/':  # redirige la ruta raíz a page1.layout
        #     return acp.actuals_layout(dic_clean_2)
        elif pathname == '/':  # redirige la ruta raíz a page1.layout
            return ol.actuals_oura_ring(complete_oura_df=complete_oura_df)
        else:
            return '404 Página no encontrada'
