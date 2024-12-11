#Personal Modules
from src.iot_project.dashboard.general_functions import subset_dataframes as sdf
from src.iot_project.dashboard.general_functions import dash_table_creator as dtc
from src.iot_project.dashboard.general_functions import styles_lists_function as slf

#Libraries
import pandas as pd
from dash.dependencies import Input, Output, State
import dash
import dash_table
import dash_html_components as html
import logging
from src.iot_project import open_ai_llm as summ

#logging
logger = logging.getLogger('myAppLogger')

#%%

DAILY_ACTIVITY_DF_COLS = [
    "score_daily_activity",
    "active_calories",
    "average_met_minutes",
    "equivalent_walking_distance",
    "high_activity_met_minutes",
    "high_activity_time",
    "inactivity_alerts",
    "low_activity_met_minutes",
    "low_activity_time",
    "medium_activity_met_minutes",
    "medium_activity_time",
    "meters_to_target",
    "non_wear_time",
    "resting_time",
    "sedentary_met_minutes",
    "sedentary_time",
    "steps",
    "target_calories",
    "target_meters",
    "total_calories",
    "meet_daily_targets",
    "move_every_hour",
    "recovery_time",
    "stay_active",
    "training_frequency",
    "training_volume",
    "interval"
]

DAILY_CARDIOVASCULAR_AGE_DF_COLS = ['vascular_age']

DAILY_READINESS_DF_COLS = [
    "score_daily_readiness",
    "activity_balance",
    "body_temperature",
    "hrv_balance",
    "previous_day_activity",
    "previous_night",
    "recovery_index",
    "resting_heart_rate",
    "sleep_balance",
    "temperature_deviation",
    "temperature_trend_deviation"
]

DAILY_SLEEPS_DF_COLS = [
    "score_daily_sleep",
    "activity_balance",
    "hrv_balance",
    "previous_day_activity",
    "previous_night",
    "recovery_index",
    "resting_heart_rate",
    "sleep_balance"
]

DAILY_SPO2_DF_COLS = [
    "breathing_disturbance_index",
    "average"
]

DAILY_STRESS_DF_COLS = [
    "stress_high",
    "recovery_high",
    "day_summary",
]

#%%

# def format_summary(final_summary):
#     """
#     Formats the OpenAI text string into a structured HTML list.
#     """
#     import dash_html_components as html  # Import necesario para generar elementos HTML

#     lines = final_summary.split('- **')  # Dividir por los títulos
#     formatted_lines = []

#     for line in lines:
#         line = line.strip()  # Limpiar espacios
#         if "**" in line:  # Asegurarse de que contenga `**`
#             try:
#                 # Dividir en título y contenido
#                 title, content = line.split("**: ", 1)
#                 formatted_lines.append(html.Li([
#                     html.Strong(f"{title.strip()}: "),
#                     content.strip()
#                 ]))
#             except ValueError:
#                 # Manejar líneas que no se pueden dividir correctamente
#                 formatted_lines.append(html.Li(line))  # Agregar línea como está
#         elif line:  # Si la línea no está vacía pero tampoco tiene formato `**Título**: contenido`
#             formatted_lines.append(html.Li(line))

#     return formatted_lines

def format_summary(text):
    """
    Procesa el texto para convertir los elementos con '**' en negritas
    y manejar bullets como una lista ordenada.
    """
    lines = text.split("\n")  # Dividir el texto en líneas
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        
        if "**" in line:  # Si contiene '**', procesar como texto con negritas
            parts = line.split("**")
            formatted_line = []
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Partes dentro de '**' van en negritas
                    formatted_line.append(html.Strong(part))
                else:  # Partes fuera de '**' van como texto plano
                    formatted_line.append(part)
            formatted_lines.append(html.Li(formatted_line))
        else:
            formatted_lines.append(html.Li(line))  # Línea sin '**', agregar como lista normal

    return formatted_lines

def create_table(n_clicks: int, 
                 selected_day: str, 
                 columns: list[str],
                 conditional_columns: list[str],
                 complete_oura_ring_df: pd.DataFrame,
                 invert_palette: bool):
    """
    Parameters
    ----------
    n_clicks : int
        number of click.
    selected_day : str
        selected day.
    columns : list[str]
        list of columns.
    conditional_columns : list[str]
        columns we want to give conditional format.
    complete_oura_ring_df : pd.DataFrame
        oura df data.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if n_clicks is None or n_clicks == 0:
        return None

    try:
        filtered_df = sdf.filter_day_columns(df=complete_oura_ring_df, 
                                             day=selected_day, 
                                             columns=columns)
        
        style_data_conditional, style_cell_conditional = slf.conditional_style(data=filtered_df,
                                                                               columns=columns,
                                                                               invert_palette=invert_palette,
                                                                               conditional_cols=conditional_columns)
        
        return dtc.data_table_for_dash(data=filtered_df, 
                                       columns=columns, 
                                       style_data_conditional=style_data_conditional, 
                                       style_cell_conditional=style_cell_conditional)
    except Exception as e:
        logger.error(f"Error processing data for day {selected_day}: {e}")
        return html.Div(f"An error occurred: {str(e)}", style={"color": "red", "textAlign": "center"})

#%%

def register_callback_actuals(app, 
                              complete_oura_ring_df: pd.DataFrame, 
                              personal_info_oura: pd.DataFrame,
                              text: str,
                              ) -> None:
    """
    Parameters
    ----------
    app : app
        Our dash app.
    complete_oura_ring_df : pd.DataFrame
        DataFrame with complete info.
    personal_info_oura : pd.DataFrame
        DataFrame with user info.
    Returns
    -------
    None

    """
    @app.callback(
        Output('daily-table', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('day-dropdown', 'value')]
    )

    def update_daily_activity_table(n_clicks, selected_day):
        return create_table(n_clicks=n_clicks, 
                            selected_day=selected_day, 
                            columns=DAILY_ACTIVITY_DF_COLS, 
                            invert_palette=False,
                            complete_oura_ring_df=complete_oura_ring_df,
                            conditional_columns=["score_daily_activity", 
                                                 "active_calories", 
                                                 "target_calories",
                                                 "total_calories"])

    @app.callback(
        Output('Daily-Readiness-table', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('day-dropdown', 'value')]
    )

    def update_daily_readiness(n_clicks, selected_day):
        return create_table(n_clicks=n_clicks, 
                            selected_day=selected_day,
                            invert_palette=False,
                            columns=DAILY_READINESS_DF_COLS, 
                            complete_oura_ring_df=complete_oura_ring_df,
                            conditional_columns=["body_temperature", 
                                                 "temperature_deviation", 
                                                 "temperature_trend_deviation"])
    
    @app.callback(
        Output('Daily-Sleep-table', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('day-dropdown', 'value')]
    )
    def update_daily_sleep(n_clicks, selected_day):
        return create_table(n_clicks=n_clicks, 
                            selected_day=selected_day,
                            invert_palette=False,
                            columns=DAILY_SLEEPS_DF_COLS, 
                            complete_oura_ring_df=complete_oura_ring_df,
                            conditional_columns=["sleep_balance", 
                                                 "hrv_balance", 
                                                 "activity_balance"])

    @app.callback(
        Output('Daily-Stress-table', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('day-dropdown', 'value')]
    )
    def update_daily_stress(n_clicks, selected_day):
        return create_table(n_clicks=n_clicks, 
                            selected_day=selected_day,
                            invert_palette=True,
                            columns=DAILY_STRESS_DF_COLS, 
                            complete_oura_ring_df=complete_oura_ring_df,
                            conditional_columns=["stress_high", 
                                                 "recovery_high"])
     
    @app.callback(
        Output('Daily-Spo2-table', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('day-dropdown', 'value')]
    )

    def update_daily_spo2(n_clicks, selected_day):
        return create_table(n_clicks=n_clicks, 
                            selected_day=selected_day, 
                            columns=DAILY_SPO2_DF_COLS,
                            invert_palette=False,
                            complete_oura_ring_df=complete_oura_ring_df,
                            conditional_columns=["average"])

    @app.callback(
        Output('Daily-Cardiovascular-table', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('day-dropdown', 'value')]
    )

    def update_daily_cardio(n_clicks, selected_day):
        return create_table(n_clicks=n_clicks, 
                            selected_day=selected_day,
                            invert_palette=False,
                            columns=DAILY_CARDIOVASCULAR_AGE_DF_COLS, 
                            complete_oura_ring_df=complete_oura_ring_df,
                            conditional_columns=["vascular_age"])

    @app.callback(
        Output('Information-User-container', 'children'),
        [Input('submit-button', 'n_clicks')]
        )

    def update_personal_info(n_clicks):
        spacing_div = html.Div(style={'height': '29px'})
        spacing_div2 = html.Div(style={'height': '10px'})

        if n_clicks is None or n_clicks == 0:
            return None
        try:
            columns_1 = ['id', 'biological_sex', 'email']
            columns_2 = ['age', 'weight', 'height']
            
            first_data = personal_info_oura.loc[:,columns_1]
            second_data = personal_info_oura.loc[:,columns_2]

            table_1 =  dash_table.DataTable(
                        data=first_data.to_dict('records'),
                        columns=[{'name': col, 'id': col} for col in first_data.columns],
                        style_cell={'textAlign': 'center','fontFamily': 'Arial'},
                        style_header={
                        'textAlign': 'center',  
                        'fontWeight': 'bold',   
                        'backgroundColor': 'rgb(230, 230, 230)', 
                        'border': '1px solid',
                        'fontFamily': 'Arial',
                        'fontSize': '14px'},
                        style_table = {'overflowX': 'auto'}
                        )
            
            table_2 =  dash_table.DataTable(
                        data=second_data.to_dict('records'),
                        columns=[{'name': col, 'id': col} for col in second_data.columns],
                        style_cell={'textAlign': 'center','fontFamily': 'Arial'},
                        style_header={
                        'textAlign': 'center',  
                        'fontWeight': 'bold',   
                        'backgroundColor': 'rgb(230, 230, 230)', 
                        'border': '1px solid',
                        'fontFamily': 'Arial',
                        'fontSize': '14px'},
                        style_table = {'overflowX': 'auto'}
                        )
            
            return html.Div([
                spacing_div2,
                table_1,
                spacing_div,
                table_2,
                spacing_div,
            ])
        except Exception as e:
            logger.error(f"Error Formatting Personal Info DataFrame: {e}")
            return html.Div(f"An error occurred: {str(e)}")

    @app.callback(
        Output('score-info-container1', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('day-dropdown', 'value')]
        )

    def score_information(n_clicks, selected_day):
        if n_clicks is None or n_clicks == 0:
            return None
        try:
            columns_score = ['score_daily_activity', 'score_daily_readiness', 'score_daily_sleep']
            score_data = complete_oura_ring_df.loc[selected_day, columns_score]
            score_data = pd.DataFrame(score_data).T
            
            return dash_table.DataTable(
                        data=score_data.to_dict('records'),
                        columns=[{'name': col, 'id': col} for col in score_data.columns],
                        style_cell={'textAlign': 'center','fontFamily': 'Arial'},
                        style_header={
                        'textAlign': 'center',  
                        'fontWeight': 'bold',   
                        'backgroundColor': 'rgb(230, 230, 230)', 
                        'border': '1px solid',
                        'fontFamily': 'Arial',
                        'fontSize': '14px'},
                        style_table = {'overflowX': 'auto'}
                        )
        except Exception as e:
            logger.error(f"Error processing data for day {selected_day}: {e}")
            return html.Div(f"An error occurred: {str(e)}", style={"color": "red", "textAlign": "center"})

    @app.callback(
        Output('personal-recomm-table', 'children'),
        Input('submit-button', 'n_clicks')
    )
    def update_recommendations(n_clicks):
        if n_clicks is None or n_clicks == 0:
            return None
        
        # json_text = complete_oura_ring_df.to_json(orient='records', lines=False, indent=4)
        # final_summary = summ.chat_gpt_summary(api_key=openai_key, input_text=json_text)
        formatted_recommendations = format_summary(text)
        # logger.info("Open AI key not given")
        # return html.Pre(text, style={'textAlign': 'left', 'margin': '10px', 'whiteSpace': 'pre-wrap', 'lineHeight': '1.6'})
        return html.Ul(formatted_recommendations, 
                   style={'textAlign': 'left', 'margin': '10px', 'lineHeight': '1.6'})

