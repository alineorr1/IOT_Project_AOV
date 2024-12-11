#Personal Modules
from src.iot_project.dashboard.general_functions import color_heatmap_for_tables as fn

#Libraries
import pandas as pd

#%%

def conditional_style(data: pd.DataFrame, 
                      columns: list,
                      conditional_cols: list,
                      invert_palette=False) -> tuple:
    """
    Parameters
    ----------
    data : pd.DataFrame
        DESCRIPTION.
    columns : list
        DESCRIPTION.
    conditional_cols : list
        DESCRIPTION.
    invert_palette : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    tuple
        DESCRIPTION.

    """
    style_data_conditional = []
    style_cell_conditional = [{'if': {'column_id': col}, 'textAlign': 'center',
                               'fontFamily': 'Arial'} for col in columns]


    # Apply Heatmap color
    for index, row in data.iterrows():
        for col in conditional_cols:
            value = row[col]

            if isinstance(value, pd.Series):
                value = value.iloc[0]

            if isinstance(value, str):
                value = value.replace('%', '').replace(',', '').strip()
                try:
                    value = float(value)
                except ValueError:
                    continue

            if pd.isna(value):
                continue

            # Estilo condicional basado en la lógica anterior
            style_data_conditional.append({
                'if': {
                    'row_index': index,
                    'column_id': col
                },
                'backgroundColor': fn.map_value_to_color_inverte_pallete_option(
                    value=value, invert_palette=invert_palette)
            })

    return style_data_conditional, style_cell_conditional
