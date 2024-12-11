#Libraries
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
from datetime import date, timedelta
import os
import dash_table
#logging config
import logging

# Logger Config
logger = logging.getLogger('myAppLogger')

#%%

# def heart_rate_layout():

#     layout = html.Div([
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4("Heart Rate Visualization", className="card-title"),
#                         html.Div("Analyze your heart rate data interactively with activity sources."),
#                         dcc.Graph(id="heart-rate-graph"),
#                         html.Div(id="hover-info", style={
#                             "textAlign": "center", "marginTop": "10px", "fontSize": "16px", "fontWeight": "bold"})
#                     ])
#                 ], className="m-3")
#             ], width=8),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4("Activity Breakdown", className="card-title"),
#                         html.Div("Explore your activity data dynamically:"),
#                         html.Div(id="activity-table-container"),
#                     ])
#                 ], className="m-3")
#             ], width=4)
#         ]),
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4("Source Mapping", className="card-title"),
#                         dcc.Markdown("""
#                         - **😴 Sleep**: Represented by low heart rate.
#                         - **🏃 Workout**: High-intensity activities.
#                         - **📚 Awake**: Typical rest or light activity periods.
#                         """, style={"fontSize": "14px"}),
#                     ])
#                 ], className="m-3")
#             ], width=12),
#         ])
#     ])
                                     
#     return layout

# def heart_rate_layout():
#     layout = html.Div([
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4("Heart Rate Visualization", className="card-title"),
#                         html.Div("Analyze your heart rate data interactively with activity sources."),
#                         dcc.Graph(id="heart-rate-graph"),
#                         html.Div(id="hover-info", style={
#                             "textAlign": "center", "marginTop": "10px", "fontSize": "16px", "fontWeight": "bold"})
#                     ])
#                 ], className="m-3")
#             ], width=8),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4("Activity Breakdown", className="card-title"),
#                         html.Div("Explore your activity data dynamically:"),
#                         html.Div(id="activity-table-container"),
#                         html.Hr(),
#                         html.H5("Data Source", style={"marginTop": "20px"}),
#                         html.Div(id="heart-rate-df-container")  # Aquí irá la tabla generada por el callback
#                     ])
#                 ], className="m-3")
#             ], width=4)
#         ]),
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4("Source Mapping", className="card-title"),
#                         dcc.Markdown("""
#                         - **😴 Sleep**: Represented by low heart rate.
#                         - **🏃 Workout**: High-intensity activities.
#                         - **📚 Awake**: Typical rest or light activity periods.
#                         """, style={"fontSize": "14px"}),
#                     ])
#                 ], className="m-3")
#             ], width=12),
#         ])
#     ])

#     return layout

def heart_rate_layout():
    layout = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Heart Rate Visualization", className="card-title"),
                        html.Div("Analyze your heart rate data interactively with activity sources."),
                        dcc.Graph(id="heart-rate-graph"),
                        html.Div(id="hover-info", style={
                            "textAlign": "center", "marginTop": "10px", "fontSize": "16px", "fontWeight": "bold"})
                    ])
                ], className="m-3")
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Activity Breakdown", className="card-title"),
                        html.Div("Explore your activity data dynamically:"),
                        html.Div(id="activity-table-container"),
                        html.Hr(),
                        html.H5("Data Source", style={"marginTop": "20px"}),
                        html.Div(id="heart-rate-df-container")  # Aquí irá la tabla generada por el callback
                    ])
                ], className="m-3")
            ], width=4)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Source Mapping", className="card-title"),
                        dcc.Markdown("""
                        - **😴 Sleep**: Represented by low heart rate.
                        - **🏃 Workout**: High-intensity activities.
                        - **📚 Awake**: Typical rest or light activity periods.
                        """, style={"fontSize": "14px"}),
                    ])
                ], className="m-3")
            ], width=12),
        ])
    ])

    return layout



