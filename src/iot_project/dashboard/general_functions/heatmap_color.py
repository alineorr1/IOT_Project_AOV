def color_for_value(value, 
                    max_value=1, 
                    min_value=-1):
    """
    Calcula el color correspondiente a un valor dado, utilizando un verde más saturado para los máximos y manteniendo los intermedios como están.
    
    :param value: El valor para el cual calcular el color.
    :param max_value: El valor máximo esperado en los datos.
    :param min_value: El valor mínimo esperado en los datos.
    :return: Un string con el código de color en formato RGB.
    """
    # Verificar si el valor es NaN y retornar un color por defecto
    # if pd.isnull(value):
    #     return 'rgba(211, 211, 211, 0.5)'  # Gris claro para indicar valor no disponible o inválido
    
    # Asegurar que max_value es mayor que min_value para evitar división por cero
    if max_value <= min_value:
        return '#d3d3d3'  # Gris claro para configuración inválida
    
    # Normalizamos el valor al rango [0, 1]
    normalized_value = (value - min_value) / (max_value - min_value)
    
    # Definimos el color del verde mas brillante y saturado para el maximo
    bright_max_green = (50, 205, 50)  # Un verde más vivo
    
    # Definimos el color del amarillo tenue para los intermedios
    mid_yellow = (255, 240, 100)
    
    # Si el valor es el mínimo, devolver rojo
    if value == min_value:
        return '#ff0000'  # Rojo intenso
    
    # Si el valor es el maximo, devolver un verde más brillante y saturado
    if value == max_value:
        return f'rgb{bright_max_green}'  # Verde más vivo
    
    # Calcular el color basado en el valor normalizado
    if normalized_value < 0.5:
        # Interpolar entre rojo y amarillo tenue
        r = 255
        g = mid_yellow[1] * normalized_value * 2
        b = mid_yellow[2] * normalized_value * 2  
    else:
        # Interpolar entre amarillo tenue y verde más brillante y saturado
        r = mid_yellow[0] * (1 - (normalized_value - 0.5) * 2)  # Reducir hacia el verde
        g = mid_yellow[1] + (bright_max_green[1] - mid_yellow[1]) * (normalized_value - 0.5) * 2  # Interpolar hacia el verde más vivo
        b = mid_yellow[2] * (1 - (normalized_value - 0.5) * 2)  # Reducir hacia el verde
    
    r, g, b = int(r), int(g), int(b)
    return f'rgb({r}, {g}, {b})'
