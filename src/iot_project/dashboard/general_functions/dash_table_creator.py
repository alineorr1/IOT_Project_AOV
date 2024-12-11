#Libraries
import pandas as pd
# Libraries
import dash_table
import logging
#logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#%%

def data_table_for_dash(data: pd.DataFrame, 
                        columns: list, 
                        style_data_conditional: list, 
                        style_cell_conditional: list, 
                        wrap_text=False, 
                        fontsize='14px'):
    """
    Create a Dash DataTable with custom styles and conditional formatting.

    Parameters
    ----------
    datos : pd.DataFrame
        DataFrame containing the data to be displayed in the table.
    columnas : list
        List of column names to be displayed in the table.
    style_data_conditional : list
        List of conditional formatting rules for the data cells.
    style_cell_conditional : list
        List of conditional formatting rules for the table cells.
    wrap_text : bool, optional
        Whether to wrap text inside the cells. Default is False.
    fontsize : str, optional
        Font size for the table header. Default is '14px'.

    Returns
    -------
    dash_table.DataTable
        A Dash DataTable with the provided data, styles, and formatting.

    """
    
    header_style = {
        'border': '1px solid #000',
        'fontWeight': 'bold',
        'background-color': '#f2f2f2',
        'textAlign': 'center',
        'fontFamily': 'Arial',
        'fontSize': fontsize,
        'whiteSpace': 'normal' if wrap_text else 'nowrap',
        'height': 'auto' if wrap_text else 'normal'
    }
    
    return dash_table.DataTable(
        data=data.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in columns],
        style_cell={'border': '1px solid #ccc', 'textAlign': 'right', 'fontFamily': 'Arial'},
        style_header=header_style,
        style_data_conditional=style_data_conditional,
        style_cell_conditional=style_cell_conditional,
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        style_table={'border-collapse': 'collapse', 'width': '100%', 'overflowX': 'auto'}
    )