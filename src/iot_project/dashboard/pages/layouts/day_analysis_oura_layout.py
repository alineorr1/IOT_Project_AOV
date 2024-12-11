# Libraries
import pandas as pd
import warnings
# Dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.io as pio

#%%

warnings.simplefilter(action="ignore", category=FutureWarning)
pio.templates.default = "plotly_white"

#%%

def actuals_oura_ring(complete_oura_df: pd.DataFrame):
    
    dropdown_options = [{'label': day, 'value': day} for day in complete_oura_df.index.strftime('%Y-%m-%d')]
    layout = html.Div([
        dcc.Store(id="store"),
        html.Div([
            html.Div(id='selected-day-container', style={'display': 'none'}),
            # html.Div(id='selected-period-container1', style={'display': 'none'}),

            # Primera fila
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4('Parameters', className='card-title'),
                            html.Label('Select a Date for Analysis:', style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id='day-dropdown',
                                options=dropdown_options,
                                placeholder="Select a period",
                                value=complete_oura_df.index.strftime('%Y-%m-%d')[-1],
                                style={'fontFamily': 'Arial'},
                                searchable=True
                            ),
                            # dcc.Dropdown(
                            #     id='ticker-dropdown1',
                            #     placeholder="Select a ticker",
                            #     style={'fontFamily': 'Arial'},
                            #     searchable=True
                            # ),
                            dbc.Row([
                                dbc.Col(
                                    html.Button('Submit', id='submit-button', n_clicks=0,
                                                className="btn btn-primary m-2",
                                                style={'fontFamily': 'Arial'}),
                                    width="auto"
                                ),
                                dbc.Col(
                                    html.Button('Download as PDF', id='download-button', n_clicks=0,
                                                className="btn btn-secondary m-2",
                                                style={'fontFamily': 'Arial'}),
                                    width="auto"
                                )
                            ], justify="start")
                        ])
                    ], className="m-3"),

                    dbc.Card([
                        dbc.CardBody([
                            html.H4('Score Information', className='card-title',
                                    style={'font-size': '24px', 'fontFamily': 'Arial'}),
                            html.Div(id='score-info-container1')
                        ])
                    ], className="m-3")
                ], width=6, style={"padding-right": ".2px"}),

                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4('Personal User Information', className='card-title'),
                            html.Div(id='Information-User-container')
                        ])
                    , className="m-3", style={"overflowX": "auto"})
                ], width=6, style={"padding-left": ".2px"})
            ], style={"margin-bottom": "1px"}),

            # Tarjeta de daily_activity, cardiovascular, readiness, sleep,
            # spo2_df and stress
            dbc.Card(
                dbc.CardBody([
                    html.Details([
                        html.Summary([
                            html.Span("Daily Activity, Daily Cardiovascular Age, Readiness, Sleep, Spo2 and Stress", 
                                      id='dynamic-summary', style={
                                          'cursor': 'pointer', 'fontFamily': 'Arial',
                                          'margin-bottom': '10px', 'fontWeight': 'bold'}),
                        ], style={'cursor': 'pointer', 'fontFamily': 'Arial',
                                  'margin-bottom': '10px'}),
                        html.Div(id='daily-table',
                                 style={"overflowX": "auto", "margin-bottom": "10px"}),
                        html.Div(id='Daily-Readiness-table',
                                 style={"margin-bottom": "10px"}),
                        html.Div(id='Daily-Sleep-table',
                                 style={"overflowX": "auto", "margin-bottom": "10px"}),
                        html.Div(id='Daily-Spo2-table',
                                 style={"overflowX": "auto", "margin-bottom": "10px"}),
                        html.Div(id='Daily-Stress-table',
                                 style={"overflowX": "auto", "margin-bottom": "10px"}),
                        html.Div(id='Daily-Cardiovascular-table',
                                 style={"margin-bottom": "10px"}),
                    ], open=True)
                ]), className="m-3", style={"margin-bottom": "1px", "margin-top": "1px"}
            ),

            # Tarjeta de Other Relevant Data
            dbc.Card(
                dbc.CardBody([
                    html.Details([
                        html.Summary("Personal Recommendation From Data", style={
                            'cursor': 'pointer', 'fontFamily': 'Arial',
                            'margin-bottom': '10px', 'fontWeight': 'bold'}),
                        html.Div(id='personal-recomm-table',
                                 style={"margin-bottom": "10px"}),
                        # html.Div(id='Others-table21')
                    ], open=True)
                ]), className="m-3", style={"margin-bottom": "1px"}
            ),

            # Tarjeta con Binary Logic y Nuevas Tablas en Columnas
            # dbc.Card(
            #     dbc.CardBody([
            #         html.Details([
            #             html.Summary("Binary Logic", style={
            #                 'cursor': 'pointer', 'fontFamily': 'Arial',
            #                 'margin-bottom': '10px'}),

            #             # Fila con dos columnas de tablas
            #             dbc.Row([
            #                 # Primera columna con tablas
            #                 dbc.Col([
            #                     html.Div(id='Historical_Growth_umbral',
            #                              style={"margin-bottom": "10px"}),
            #                     html.Div(id='Growth_vs_peers_umbral',
            #                              style={"margin-bottom": "10px"}),
            #                     html.Div(id='Estimated_Growth_umbral',
            #                              style={"margin-bottom": "10px"}),
            #                     html.Div(id='Historical_Valuation_umbral',
            #                              style={"margin-bottom": "10px"}),
            #                     html.Div(id='Valuation_vs_peers_umbral',
            #                              style={"margin-bottom": "10px"}),
            #                 ], width=6),

            #                 # Segunda columna con nuevas tablas
            #                 dbc.Col([
            #                     html.Div(id='Debt_ratios_umbral',
            #                              style={"margin-bottom": "10px"}),
            #                     html.Div(id='Profitability_umbral',
            #                              style={"margin-bottom": "10px"}),
            #                     html.Div(id='Margins_umbral',
            #                              style={"margin-bottom": "10px"}),
            #                     html.Div(id='Other_umbral',
            #                              style={"margin-bottom": "10px"})
            #                 ], width=6)
            #             ])  # Cierre de dbc.Row
            #         ], open=False)
            #     ]), className="m-3", style={"margin-bottom": "1px"}
            # )
        ])
    ])
    return layout