#Personal Modules
from src.iot_project.providers.google import google_api_example as gg

#Libraries
from dash.dependencies import Input, Output
import plotly.express as px
import dash_html_components as html
import dash_table
import pandas as pd
#logging config
import logging

# Logger Config
logger = logging.getLogger('myAppLogger')

#%%

def register_weather_callbacks(app, api_key: str = None):
    location_map = {
        "mexico": {"latitude": 19.4326, "longitude": -99.1332},
        "uk": {"latitude": 51.5074, "longitude": -0.1278}
    }

    static_dataframes = {
        "mexico": pd.read_csv("Input/mexico_weather.csv", index_col=0),
        "uk": pd.read_csv("Input/uk_weather.csv", index_col=0)
    } if api_key is None else {}
        
    @app.callback(
        [Output("location-info", "children"),
         Output("weather-graph", "figure"),
         Output("weather-df-container", "children")],
        Input("location-dropdown", "value")
    )
    def update_weather(selected_location):
        try:
            location = location_map[selected_location]
            location_text = f"Selected Location: {selected_location.capitalize()} ({location['latitude']}, {location['longitude']})"

            if api_key:
                weather_df = gg.historical_weather_data(api_key=api_key, location_dict=location)
            else:
                weather_df = static_dataframes.get(selected_location)
                if weather_df is None:
                    raise ValueError(f"Static data not found for {selected_location.capitalize()}.")

            if weather_df.empty:
                raise ValueError(f"No data available for {selected_location.capitalize()}.")

            fig = px.bar(
                weather_df,
                x="dateTime",
                y="index_1_aqi",
                color="index_1_category",
                title=f"Air Quality Index (AQI) in {selected_location.capitalize()}",
                labels={"index_1_aqi": "AQI", "dateTime": "Time", "index_1_category": "Category"},
                hover_data=["index_1_aqi", "index_1_category"]
            )
            fig.update_layout(
                xaxis_title="Date and Time",
                yaxis_title="AQI",
                legend_title="Air Quality Category",
                width=1200,
                height=600
            )

            # Crear tabla dinámica
            weather_table = dash_table.DataTable(
                id="weather-df-table",
                columns=[{"name": col, "id": col} for col in weather_df.columns],
                data=weather_df.to_dict("records"),
                style_table={"height": "500px", "overflowY": "auto"},
                style_header={
                    "backgroundColor": "rgb(230, 230, 230)",
                    "fontWeight": "bold",
                    "textAlign": "center"
                },
                style_cell={
                    "textAlign": "center",
                    "fontFamily": "Arial",
                    "padding": "10px",
                    "fontSize": "12px"
                },
                fixed_rows={"headers": True}
            )

            return location_text, fig, weather_table

        except ValueError as ve:
            error_message = f"Error: {ve}"
            return error_message, px.Figure(), html.Div("No data available.")

        except Exception as e:
            error_message = f"Failed to fetch data for {selected_location.capitalize()}. Error: {e}"
            return error_message, px.Figure(), html.Div("No data available.")

    @app.callback(
        Output("category-summary", "children"),
        Input("weather-graph", "hoverData")
    )
    def update_category_summary(hover_data):
        if hover_data is None:
            return "Hover over a bar to see category details."

        try:
            point = hover_data["points"][0]
            category = point["customdata"][0]
            aqi = point["y"]
            date_time = point["x"]

            return html.Div([
                html.P(f"Date and Time: {date_time}"),
                html.P(f"Air Quality Index (AQI): {aqi}"),
                html.P(f"Category: {category}")
            ])
        except Exception as e:
            return html.Div(f"An error occurred while processing hover data: {e}", style={"color": "red"})
