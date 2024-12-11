# Personal Modules
# import src.modules.plotting as gp
# import src.modules.aux_functions as fn
from src.iot_project.modules import visualizations as vs
from src.iot_project.dashboard.general_functions import heatmap_color as gf
from src.iot_project.modules import correlation_df as cr

# Libraries
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_table
import logging
import pandas as pd
import dash_html_components as html

# Logger Config
logger = logging.getLogger('myAppLogger')

#%%

# Callbacks
_cached_corr_df = None

def historical_oura_analysis_callback(app, 
                                      complete_oura_ring_df: pd.DataFrame):
    
    global _cached_corr_df

    if _cached_corr_df is None:
            _cached_corr_df = cr.correlation_matrix(df_x=complete_oura_ring_df)
            logger.info("Correlation matrix calculated and cached.")
    avail_cols = list(complete_oura_ring_df.columns)
    # corr_df = cr.correlation_matrix(df_x=complete_oura_ring_df)
    
    @app.callback(
    Output('second-col-line', 'options'),
    Input('first-col-line', 'value')
    )

    def update_second_col_options(selected_first_col):
        filtered_options = [{'label': col, 'value': col} for col in avail_cols if col != selected_first_col and col != 'day' and col != 'day_summary']
        return filtered_options
    
    @app.callback(
        Output('double-line-graph', 'children'),
        [Input('plot-button', 'n_clicks')],
        [State('first-col-line', 'value'),
         State('second-col-line', 'value')]
    )
    def double_axis_line_plot(n_clicks, first_col: str, second_col: str):
        if n_clicks is None or n_clicks == 0:
            return html.Div("Select columns and click Submit to generate the plot.", 
                            style={'textAlign': 'center', 'marginTop': '20px'})
    
        if not first_col or not second_col:
            return html.Div("Please select both columns before generating the plot.", 
                            style={'color': 'red', 'textAlign': 'center', 'marginTop': '20px'})
    
        try:
            fig = vs.timeline_shared_axis(df=complete_oura_ring_df, 
                                          first_col=first_col, 
                                          second_col=second_col)
    
            return dcc.Graph(figure=fig)
        except Exception as e:
            logger.error(f"Error generating double axis line plot: {e}")
            return html.Div(f"An error occurred: {e}", style={'color': 'red', 'textAlign': 'center'})
        
        
    @app.callback(
        Output('timeseries-output', 'children'),
        [Input('plot-button', 'n_clicks')],
        [State('line-chart-col', 'value')]
        )    
    
    def line_plot(n_clicks, col: str):
        if n_clicks is None or n_clicks == 0:
            return html.Div("Select a column and click Submit to generate the plot.", 
                            style={'textAlign': 'center', 'marginTop': '20px'})
        
        if not col:
            return html.Div("Please select a column before generating the plot.", 
                            style={'color': 'red', 'textAlign': 'center', 'marginTop': '20px'})
    
        try:

            fig = vs.line_chart(
                df=complete_oura_ring_df,
                x_col='day',       
                y_col=col,
                title=f"Line Chart for {col}"
            )
            
            return dcc.Graph(figure=fig)
        except Exception as e:
            logger.error(f"Error generating line plot: {e}")
            return html.Div(f"An error occurred: {e}", style={'color': 'red', 'textAlign': 'center'})
    
    @app.callback(
    Output('y-col-scatter', 'options'),   # Actualiza las opciones del dropdown
    [Input('x-col-scatter', 'value')]    # Observa el valor seleccionado en x-col-scatter
    )

    def update_y_col_options(selected_x_col):
        # Si no hay selección, muestra todas las columnas
        if not selected_x_col:
            return [{'label': col, 'value': col} for col in avail_cols]
        
        # Excluir la columna seleccionada en x-col-scatter
        return [{'label': col, 'value': col} for col in avail_cols if col != selected_x_col and col != 'day' and col != 'day_summary']

    @app.callback(
        Output('extra-output', 'children'),
        [Input('plot-button', 'n_clicks')],
        [State('x-col-scatter', 'value'),
         State('y-col-scatter', 'value')]
    )
    def scatter_plot_callback(n_clicks, x_col: str, y_col: str):
        if n_clicks is None or n_clicks == 0:
            return html.Div("Select columns and click Submit to generate the plot.", 
                            style={'textAlign': 'center', 'marginTop': '20px'})
        
        if not x_col or not y_col:
            return html.Div("Please select both X and Y columns before generating the plot.", 
                            style={'color': 'red', 'textAlign': 'center', 'marginTop': '20px'})
    
        try:
            # Generar el scatter plot
            fig = vs.scatter_plot(
                df=complete_oura_ring_df,
                x_col=x_col,
                y_col=y_col,
                x_label=x_col, 
                y_label=y_col, 
                title=f"Scatter Plot: {y_col} vs {x_col}"
                )
            
            return dcc.Graph(figure=fig)
        except Exception as e:
            logger.error(f"Error generating scatter plot: {e}")
            return html.Div(f"An error occurred: {e}", style={'color': 'red', 'textAlign': 'center'})


    # @app.callback(
    #     Output('heatmap-output', 'children'),
    #     [Input('plot-button', 'n_clicks')],
    # )

    # def heatmap_df(n_clicks):
    #     if n_clicks is None or n_clicks == 0:
    #         return html.Div("Select columns and click Submit to generate the plot.", 
    #                         style={'textAlign': 'center', 'marginTop': '20px'})
        
    #     style_data_conditional = [
    #         {
    #             'if': {'row_index': i, 'column_id': column},
    #             'backgroundColor': gf.color_for_value(corr_df.at[idx, column])
    #         }
    #         for i, idx in enumerate(corr_df.index)  
    #         for column in corr_df.columns
    #         ]
        
    #     corr_df.reset_index(inplace=True)
    #     # html.H4('Correlation Heatmap', style={'textAlign': 'center', 'marginBottom': '20px'}),
    #     table = dash_table.DataTable(
    #         data=corr_df.to_dict('records'),
    #         columns=[{'name': i, 'id': i} for i in corr_df.columns],
    #         fixed_columns={'headers': True, 'data': 1},  # Fija la primera columna (índice)
    #         style_table={
    #             'overflowX': 'auto',
    #             'overflowY': 'auto',  # Habilita scroll vertical
    #             'minWidth': '100%',  # Permite scroll horizontal
    #             'margin': '0 auto',
    #             # 'marginTop': '50px',  # Espacio superior adicional
    #         },
    #         style_cell_conditional=style_data_conditional,
    #         style_data={
    #             'textAlign': 'center',
    #             'fontFamily': 'Arial',
    #         },
    #         style_cell={
    #             'minWidth': '150px', 'maxWidth': '200px', 'width': '150px',
    #             'textOverflow': 'ellipsis'# Fija ancho de columnas
    #         },
    #         # style_header={
    #         #     'fontWeight': 'bold',
    #         #     'textAlign': 'center',
    #         #     'fontFamily': 'Arial',
    #         # },
    #         style_header={
    #             'fontWeight': 'bold',
    #             'textAlign': 'center',
    #             'fontFamily': 'Arial',
    #             'whiteSpace': 'normal',  # Permite ajuste de texto
    #             'height': 'auto',        # Ajusta la altura del encabezado automáticamente
    #         },
    #         page_current=0,
    #         page_size=12,
    #     )
    @app.callback(
    Output('heatmap-output', 'children'),
    [Input('plot-button', 'n_clicks')],
    )
    def heatmap_df(n_clicks):
        if n_clicks is None or n_clicks == 0:
            return html.Div("Select columns and click Submit to generate the plot.", 
                            style={'textAlign': 'center', 'marginTop': '20px'})
    
        style_data_conditional = [
            {
                'if': {'row_index': i, 'column_id': column},
                'backgroundColor': gf.color_for_value(_cached_corr_df.at[idx, column])
            }
            for i, idx in enumerate(_cached_corr_df.index)  
            for column in _cached_corr_df.columns
        ]
    
        corr_df_display = _cached_corr_df.reset_index()
        table = dash_table.DataTable(
            data=corr_df_display.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in corr_df_display.columns],
            fixed_columns={'headers': True, 'data': 1},
            style_table={
                'overflowX': 'auto',
                'overflowY': 'auto',
                'minWidth': '100%',
                'margin': '0 auto',
            },
            style_cell_conditional=style_data_conditional,
            style_data={
                'textAlign': 'center',
                'fontFamily': 'Arial',
            },
            style_cell={
                'minWidth': '150px', 'maxWidth': '200px', 'width': '150px',
                'textOverflow': 'ellipsis'
            },
            style_header={
                'fontWeight': 'bold',
                'textAlign': 'center',
                'fontFamily': 'Arial',
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            page_current=0,
            page_size=12,
        )
        
        return table