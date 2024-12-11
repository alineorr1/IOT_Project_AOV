# DecilAnalysis.py:
# Libraries

# Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd   

import logging
#logging config
logger = logging.getLogger('myAppLogger')

#%%

def historical_oura(complete_oura_ring_df: pd.DataFrame):
    avail_cols = list(complete_oura_ring_df.columns)

    layout = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Parameters', className='card-title'),

                        # Dropdown for line chart column
                        html.Label('Select a column for Line Chart:', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='line-chart-col',
                            options=[
                                {'label': col, 'value': col} 
                                for col in complete_oura_ring_df.columns if col != 'day' and col != 'day_summary'
                            ],                            
                            # value=complete_oura_ring_df.columns[-1] if 'day' not in complete_oura_ring_df.columns else complete_oura_ring_df.columns[-2],
                            style={'fontFamily': 'Arial'}
                        ),

                        # Dropdown for X-axis of scatter plot
                        html.Label('Select X-axis for Scatter Plot:', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='x-col-scatter',
                            options=[{'label': col, 'value': col} for col in avail_cols if col != 'day'],
                            # value=avail_cols[0],
                            style={'fontFamily': 'Arial'}
                        ),

                        # Dropdown for Y-axis of scatter plot
                        html.Label('Select Y-axis for Scatter Plot:', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='y-col-scatter',
                            style={'fontFamily': 'Arial'}
                        ),

                        # Dropdown for first column in double line chart
                        html.Label('Select First Column for Line Chart:', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='first-col-line',
                            style={'fontFamily': 'Arial'},
                            options=[{'label': col, 'value': col} for col in avail_cols],
                        ),

                        # Dropdown for second column in double line chart
                        html.Label('Select Second Column for Line Chart:', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='second-col-line',
                            style={'fontFamily': 'Arial'},
                            options=[{'label': col, 'value': col} for col in avail_cols],
                        ),

                        # Submit button
                        html.Button('Submit', id='plot-button', n_clicks=0, className="btn btn-primary m-2"),
                    ])
                ], className="m-3"),   

                dbc.Card(
                    dbc.CardBody(
                        html.Div([
                            html.H4('Score Information', className='card-title'),
                            html.Div(id='extra-card')
                        ])
                    ), className="m-3"),
            ], width=6),

            dbc.Col([  
                html.Div(id='extra-output'),
            ], width=6),
        ]),

        dbc.Row([
            dbc.Col([  
                html.Div(id='double-line-graph'),
            ], width=6),
            dbc.Col([  
                html.Div(id='timeseries-output'),
            ], width=6),
        ]),
        dbc.Row([
            dbc.Col([
                html.H4('Correlation Heatmap', style={'textAlign': 'center', 
                                                      'marginBottom': '10px',
                                                      'fontFamily': 'Arial',
                                                      'fontSize': '16px'}),
                html.Div(id='heatmap-output', style={'overflowX': 'scroll', 
                                                     'maxWidth': '100%', 
                                                     'marginTop':'70px',
                                                     'margin': '0 auto',
                                                     # 'width': '50%'
                                                     }),
            ], width=12),
        ]),
    ])

    return layout