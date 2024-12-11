# Libraries
import pandas as pd
import warnings
# Dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.io as pio
import dash_html_components as html

#%%

# def weather_layout():
#     layout = html.Div([
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4("Air Quality Analysis", className="card-title"),
#                         dcc.Dropdown(
#                             id="location-dropdown",
#                             options=[
#                                 {"label": "Mexico", "value": "mexico"},
#                                 {"label": "UK", "value": "uk"}
#                             ],
#                             value="mexico",  # Valor predeterminado
#                             style={"fontFamily": "Arial", "marginBottom": "10px"}
#                         ),
#                         html.Div(id="location-info", style={
#                             "textAlign": "center", "marginBottom": "20px", "fontSize": "16px"}),
#                         dcc.Graph(id="weather-graph"),
#                     ])
#                 ], className="m-3")
#             ], width=8),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4("Air Quality Category", className="card-title"),
#                         html.Div("Explore air quality by category dynamically."),
#                         html.Div(id="category-summary", style={
#                             "textAlign": "left", "marginTop": "10px", "fontSize": "14px"})
#                     ])
#                 ], className="m-3")
#             ], width=4)
#         ])
#     ])
#     return layout

def weather_layout():
    layout = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Air Quality Analysis", className="card-title"),
                        dcc.Dropdown(
                            id="location-dropdown",
                            options=[
                                {"label": "Mexico", "value": "mexico"},
                                {"label": "UK", "value": "uk"}
                            ],
                            value="mexico",  # Valor predeterminado
                            style={"fontFamily": "Arial", "marginBottom": "10px"}
                        ),
                        html.Div(id="location-info", style={
                            "textAlign": "center", "marginBottom": "20px", "fontSize": "16px"}),
                        dcc.Graph(id="weather-graph"),
                    ])
                ], className="m-3")
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Air Quality Category", className="card-title"),
                        html.Div("Explore air quality by category dynamically."),
                        html.Div(id="category-summary", style={
                            "textAlign": "left", "marginTop": "10px", "fontSize": "14px"}),
                        html.Hr(),
                        html.H5("Data Source", style={"marginTop": "20px"}),
                        html.Div(
                            id="weather-df-container",  # Contenedor para la tabla dinámica
                            style={
                                "height": "300px",  # Altura fija con scroll
                                "overflowY": "auto",
                                "marginTop": "10px"
                            }
                        )
                    ])
                ], className="m-3")
            ], width=4)
        ])
    ])
    return layout