#Libraries
import pandas as pd

#%%

def map_value_to_color_inverte_pallete_option(value, 
                                              invert_palette=False): 
    """
    Maps a numeric value to a specific RGBA color, with optional inversion of the color palette.

    Parameters
    ----------
    value : float or str
        The value to be mapped to a color. If the value is a string, it will be 
        cleaned of any '%' characters and converted to a float. Non-numeric values 
        will result in an empty string being returned.
    invert_palette : bool, optional
        If True, the color palette will be inverted (swapping red and green components).
        Default is False.

    Returns
    -------
    str
        A string representing the RGBA color corresponding to the value, or an empty string
        if the value is not valid. The color ranges as follows:
        - Negative values result in shades of red.
        - Values between -5 and 5 return a yellow color.
        - Positive values result in shades of green.
        - The intensity of the color increases based on the magnitude of the value.
        - The `invert_palette` option swaps red and green for both negative and positive values.

    """    
    if isinstance(value, str):
        value = value.replace('%', '').strip()
        try:
            value = float(value)
        except ValueError:
            return ""

    if pd.isna(value):
        return ""
    elif value < 0:
        intensity = min(1, abs(value) / 10)
        intensity = intensity ** 0.5
        red = 255
        green = int(255 * (1 - intensity))
        blue = green
        if invert_palette:
            red, green = green, red  
        return f'rgba({red}, {green}, {blue}, 0.8)'
    elif -5 <= value <= 5:
        return 'rgba(255, 255, 0, 0.5)'
    else:
        if value < 5:
            intensity = value / 5
            red = int(255 * (1 - intensity))
            green = 255
            blue = red
            if invert_palette:
                green, red = red, green  
        else:
            intensity = min(1, value / 100)
            red = int(255 * (1 - intensity))
            green = 255
            blue = red
            if invert_palette:
                green, red = red, green  
        return f'rgba({red}, {green}, {blue}, 0.8)'    
