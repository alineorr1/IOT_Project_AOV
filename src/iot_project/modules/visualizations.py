#Libraries
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.offline as offline
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#%%

def plot_activity_time_distribution(df: pd.DataFrame) -> None:
    """
    Plot the distribution of activity times (low, medium, high intensity) as a bar chart.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'low_activity_time', 'medium_activity_time', 
                           and 'high_activity_time'.

    Returns:
        None: Displays the plot.
    """
    activity_data = df[['low_activity_time', 'medium_activity_time', 'high_activity_time']].sum()
    activity_data.plot(kind='bar', figsize=(10, 6))
    plt.title("Activity Time Distribution")
    plt.xlabel("Activity Levels")
    plt.ylabel("Total Time (minutes)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_steps_vs_active_calories(df: pd.DataFrame) -> None:
    """
    Plot a scatter plot showing the relationship between steps and active calories.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'steps' and 'active_calories'.

    Returns:
        None: Displays the scatter plot.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='steps', y='active_calories')
    plt.title("Steps vs. Active Calories")
    plt.xlabel("Steps")
    plt.ylabel("Active Calories")
    plt.tight_layout()
    plt.show()

def plot_correlation_matrix(df: pd.DataFrame) -> None:
    """
    Plot a heatmap of the correlation matrix for numerical columns in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing numerical data.

    Returns:
        None: Displays the correlation heatmap.
    """
    numerical_columns = df.select_dtypes(include=['float', 'int']).columns
    correlation_matrix = df[numerical_columns].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.show()

def plot_active_time_percentage(df: pd.DataFrame) -> None:
    """
    Plot the distribution of active time percentage as a histogram.

    Args:
        df (pd.DataFrame): DataFrame containing the column 'active_time_percentage'.

    Returns:
        None: Displays the histogram.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(df['active_time_percentage'].dropna(), bins=15, edgecolor='black')
    plt.title("Distribution of Active Time Percentage")
    plt.xlabel("Active Time Percentage (%)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

def plot_distance_per_step(df: pd.DataFrame) -> None:
    """
    Plot the distribution of distance efficiency (distance per step) as a boxplot.

    Args:
        df (pd.DataFrame): DataFrame containing the column 'distance_per_step'.

    Returns:
        None: Displays the boxplot.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='distance_per_step')
    plt.title("Distribution of Distance Efficiency (Distance per Step)")
    plt.xlabel("Distance per Step")
    plt.tight_layout()
    plt.show()

def plot_recovery_to_activity_ratio(df: pd.DataFrame) -> None:
    """
    Plot the relationship between recovery time and high activity time as a scatter plot.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'recovery_time' and 'high_activity_time'.

    Returns:
        None: Displays the scatter plot.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='high_activity_time', y='recovery_time')
    plt.title("Recovery Time vs. High Activity Time")
    plt.xlabel("High Activity Time (minutes)")
    plt.ylabel("Recovery Time (minutes)")
    plt.tight_layout()
    plt.show()

def plot_calories_target_percentage(df: pd.DataFrame) -> None:
    """
    Plot the percentage of calorie target achieved as a bar chart.

    Args:
        df (pd.DataFrame): DataFrame containing the column 'calories_target_percentage'.

    Returns:
        None: Displays the bar chart.
    """
    df['calories_target_percentage'].plot(kind='bar', figsize=(10, 6), color='skyblue', edgecolor='black')
    plt.title("Calories Target Percentage Achieved")
    plt.xlabel("Day Index")
    plt.ylabel("Percentage (%)")
    plt.tight_layout()
    plt.show()

def plot_inactivity_alerts_vs_sedentary_time(df: pd.DataFrame) -> None:
    """
    Plot the relationship between inactivity alerts and sedentary time as a scatter plot.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'inactivity_alerts' and 'sedentary_time'.

    Returns:
        None: Displays the scatter plot.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='sedentary_time', y='inactivity_alerts')
    plt.title("Inactivity Alerts vs. Sedentary Time")
    plt.xlabel("Sedentary Time (minutes)")
    plt.ylabel("Inactivity Alerts")
    plt.tight_layout()
    plt.show()

def plot_scatter_relationship(
    df: pd.DataFrame, 
    x_column: str, 
    y_column: str, 
    title: str = None
) -> None:
    """
    Plot a scatter plot for the relationship between two variables.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        x_column (str): Name of the column for the x-axis.
        y_column (str): Name of the column for the y-axis.
        title (str, optional): Title for the scatter plot. Defaults to None.

    Returns:
        None: Displays the scatter plot.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_column, y=y_column)
    plt.title(title if title else f"{x_column} vs. {y_column}")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.tight_layout()
    plt.show()

"""
steps vs. active_calories:

Para observar si un mayor número de pasos contribuye a quemar más calorías.
sedentary_time vs. inactivity_alerts:

Relación entre tiempo sedentario y las alertas de inactividad.
recovery_time vs. high_activity_time:

Ver si días con más actividad intensa requieren más tiempo de recuperación.
distance_per_step vs. steps:

Para evaluar si un aumento en los pasos está asociado con una mayor eficiencia de distancia.
active_time_percentage vs. calories_target_percentage:

Relación entre el tiempo activo y el cumplimiento de objetivos calóricos.
"""

def plot_time_series(
    df: pd.DataFrame, 
    date_column: str, 
    value_columns: list, 
    title: str = "Time Series Plot"
) -> None:
    """
    Plot a time series for one or multiple variables.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        date_column (str): Name of the column representing the date/time.
        value_columns (list): List of column names to plot as time series.
        title (str): Title for the plot.

    Returns:
        None: Displays the time series plot.
    """
    plt.figure(figsize=(12, 6))
    for col in value_columns:
        plt.plot(df[date_column], df[col], label=col)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()
    plt.show()

"""
Variables relevantes para analizar a lo largo del tiempo
steps:

Para observar patrones diarios o semanales en actividad física.
active_calories:

Tendencias en quema calórica a lo largo del tiempo.
sedentary_time y active_time_percentage:

Comparar la evolución del tiempo sedentario y el porcentaje de tiempo activo.
calories_target_percentage y distance_target_percentage:

Análisis del cumplimiento de objetivos a través del tiempo.
"""

# Relación entre pasos y calorías activas
# plot_scatter_relationship(df, 'steps', 'active_calories', title="Steps vs. Active Calories")

# Relación entre tiempo sedentario y alertas de inactividad
# plot_scatter_relationship(df, 'sedentary_time', 'inactivity_alerts', title="Sedentary Time vs. Inactivity Alerts")

# Evolución de pasos y calorías activas a lo largo del tiempo
# plot_time_series(df, date_column='day', value_columns=['steps', 'active_calories'], 
#                  title="Steps and Active Calories Over Time")

# Evolución del tiempo activo y sedentario
# plot_time_series(df, date_column='day', value_columns=['active_time_percentage', 'sedentary_time'], 
#                  title="Active Time Percentage and Sedentary Time Over Time")

#%%

def plot_correlation_heatmap(df: pd.DataFrame, 
                             title: str = "Correlation Heatmap", 
                             color_scale: str = "Viridis") -> None:
    """
    Generate and display a heatmap of the correlation matrix for a given DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing numerical data for correlation analysis.
    title : str, optional
        Title of the heatmap (default is "Correlation Heatmap").
    color_scale : str, optional
        Name of the Plotly color scale to use (default is "Viridis").

    Returns
    -------
    None
    """
    numerical_df = df.select_dtypes(include=['number'])
    
    if numerical_df.empty:
        raise ValueError("The DataFrame contains no numerical columns for correlation analysis.")
    
    numerical_df = numerical_df.loc[:, numerical_df.nunique() > 1]
    
    if numerical_df.empty:
        raise ValueError("No columns with variance available for correlation analysis after filtering.")

    corr_matrix = numerical_df.corr()
    
    fig = px.imshow(
        corr_matrix,
        color_continuous_scale=color_scale,
        zmin=-1,
        zmax=1,
        title=title,
        labels=dict(color="Correlation"),
        x=numerical_df.columns,
        y=numerical_df.columns,
        aspect="auto",
    )
    
    # Update layout for better presentation
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Variables",
        yaxis_title="Variables",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        coloraxis_colorbar=dict(title="Correlation"),
    )
    offline.plot(fig)

    # fig.show()


def timeline_shared_axis(df: pd.DataFrame, 
                         first_col: str,
                         second_col: str,
                         x_column: str = 'day',
                         ) -> None:

    
    # Asegurarse de que el x_column sea datetime
    df[x_column] = pd.to_datetime(df[x_column])
    
    # Crear subplots (uno por cada columna)
    fig = make_subplots(
        rows=2,  # Dos subplots
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,  # Espacio entre subplots
    )
    
    # Primera gráfica: 'score_daily_activity'
    fig.add_trace(
        go.Scatter(
            x=df[x_column],
            y=df[first_col],
            mode="markers+lines",
            marker=dict(symbol='circle', size=8),
            name=first_col,
            # hovertemplate=(
            #     # "<b>Date:</b> %{x|%Y-%m-%d}<br>"
            #     "<b>first_col:</b> %{y}<br>"
            #     "<b>second_col:</b> %{customdata[1]}<br><extra></extra>"
            # ),
            hovertemplate=(
                # "<b>Date:</b> %{x|%Y-%m-%d}<br>"
                "<b>" + first_col + ":</b> %{y}<br>"
                "<b>" + second_col + ":</b> %{customdata[1]}<br><extra></extra>"
            ),
            customdata=df[[first_col, second_col]].values,
            # hovertemplate='%{y:.2f}'
        ),
        row=1,
        col=1,
    )
    

    fig.update_layout(hovermode='x unified')
    
    
    # Configurar spikes para ambas gráficas
    fig.update_xaxes(
        showspikes=True,
        spikemode="across",  # Crosshair vertical sincronizado
        spikesnap="cursor",
        spikethickness=1,
        spikecolor="gray",
        spikedash="dot",
        row=1,
        col=1,
    )
    fig.update_yaxes(
        showspikes=True,
        spikemode="across",  # Crosshair vertical sincronizado
        spikesnap="cursor",
        spikethickness=1,
        spikecolor="gray",
        spikedash="dot",
        row=1,
        col=1,
    )
    
    # fig.update_layout(
    #     yaxis_title=first_col,
    #     xaxis_showgrid=True,
    #     yaxis_showgrid=True,
    #     showlegend=True,
    #     plot_bgcolor='white',
    #     paper_bgcolor='white',
    #     font_color='black',
    #     shapes=[dict(type='rect', xref='paper', x0=0, x1=1, y0=0, y1=1, fillcolor='black', layer='below')]
    # ),

    # Segunda gráfica: 'active_calories'
    fig.add_trace(
        go.Scatter(
            x=df[x_column],
            y=df[second_col],
            mode="markers+lines",
            marker=dict(symbol='circle', size=8),
            name=second_col,
            # hovertemplate=(
            #     # "<b>Date:</b> %{x|%Y-%m-%d}<br>"
            #     "<b>first_col:</b> %{y}<br>"
            #     "<b>second_col:</b> %{customdata[0]}<br><extra></extra>"
            # ),
            hovertemplate=(
                "<b>Date:</b> %{x|%Y-%m-%d}<br>"
                "<b>" + first_col + ":</b> %{y}<br>"
                "<b>" + second_col + ":</b> %{customdata[1]}<br><extra></extra>"
            ),
            customdata=df[[first_col, second_col]].values,
            # hovertemplate='%{y:.2f}'

        ),
        row=2,
        col=1,
    )
    
    fig.update_xaxes(showspikes=True, spikemode="across", spikesnap="cursor", spikethickness=0.5, 
                      spikecolor="gray", spikedash="dot", row=2, col=1)
    fig.update_layout(
        #height=600, width=1400,
        hovermode = "x unified",
        legend_traceorder="normal")
    
    fig.update_traces(xaxis='x2')
    fig.update_xaxes(showspikes=True, spikemode="across", spikesnap="cursor", 
                      spikethickness=0.5, spikecolor="gray", spikedash="dot", row=1, col=1)
    # fig.update_layout(hovermode='y unified')
    
    fig.update_layout(
    title=dict(
        text="Shared Axis Timeline",
        x=0.5,
        font=dict(
            size=15,
            family="Arial",
            color="black"
        )
    ),
    # xaxis_title="Date",
    # yaxis_title="Values",
    margin=dict(l=40, r=40, t=80, b=40)

    )
    
    # fig.update_layout(
    #     yaxis_title=second_col,
    #     xaxis_showgrid=True,
    #     yaxis_showgrid=True,
    #     showlegend=True,
    #     plot_bgcolor='white',
    #     paper_bgcolor='white',
    #     font_color='black',
    #     shapes=[dict(type='rect', xref='paper', x0=0, x1=1, y0=0, y1=1, fillcolor='black', layer='below')]
    # ),

    # Mostrar la figura
    # offline.plot(fig)
    return fig

def line_chart(df: pd.DataFrame, 
               x_col: str, 
               y_col: str,
               x_label: str = "Time", 
               title: str = "Line Chart") -> None:
    """
    Creates a professional line chart.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        x_col (str): Column name for the x-axis.
        y_col (str): Column name for the y-axis.
        x_label (str): Label for the x-axis. Default is "Time".
        y_label (str): Label for the y-axis. Default is "Value".
        title (str): Title of the chart. Default is "Line Chart".

    Returns:
        None: Displays the chart in the browser.
    """
    fig = go.Figure()

    # Add trace
    fig.add_trace(
        go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            marker=dict(size=6),
            line=dict(width=2),
            name=y_col,
            hovertemplate=                
            ("<b>Date:</b> %{x|%Y-%m-%d}<br>"
            # "<b>" + x_col + ":</b> %{y}<br>"
            "<b>" + y_col + ":</b> %{customdata[1]}<br><extra></extra>"),
            customdata=df[[x_col, y_col]].values,
        )
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(
                size=15,
                family="Arial",  # Cambiar la fuente a Arial
                color="black"    # Puedes cambiar el color si lo deseas
            )
        ),
        xaxis=dict(
            title=dict(
                text=x_label,
                font=dict(size=15, family="Arial"),  # Reduce el tamaño a 10
            ),
            showgrid=True,
            # gridcolor='lightgrey'
        ),        
        yaxis=dict(title=y_col, showgrid=True, gridcolor='lightgrey'),
        template='plotly_white',
        # hovermode='x unified',
        legend=dict(title="Legend", orientation="h", yanchor="bottom", x=0.5, xanchor="center"),
        margin=dict(l=40, r=40, t=80, b=35)
    )
    # fig.update_traces(hovertemplate=f"<b>{x_label}:</b> {{x}}<br><b>{y_label}:</b> {{y}}<extra></extra>")
    # offline.plot(fig)
    
    return fig

def scatter_plot(df: pd.DataFrame, 
                 x_col: str, 
                 y_col: str, 
                 x_label: str, 
                 y_label: str, 
                 title: str = "Scatter Plot") -> None:
    """
    Creates a professional scatter plot.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        x_col (str): Column name for the x-axis.
        y_col (str): Column name for the y-axis.
        x_label (str): Label for the x-axis. Default is "X-Axis".
        y_label (str): Label for the y-axis. Default is "Y-Axis".
        title (str): Title of the chart. Default is "Scatter Plot".

    Returns:
        None: Displays the chart in the browser.
    """
    fig = go.Figure()

    # Add trace
    fig.add_trace(
        go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(size=8, color='blue', opacity=0.7),
            name=f"{y_col} vs {x_col}",
            hovertemplate=                
            ("<b>Date:</b> %{x|%Y-%m-%d}<br>"
            "<b>" + x_col + ":</b> %{x}<br>"
            "<b>" + y_col + ":</b> %{customdata[1]}<br><extra></extra>"),
            customdata=df[[x_col, y_col]].values,

        )
    )

    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(
                size=15,
                family="Arial",  # Cambiar la fuente a Arial
                color="black"    # Puedes cambiar el color si lo deseas
            )
        ),
        # xaxis=dict(title=x_label, showgrid=True, gridcolor='lightgrey'),
        
        xaxis=dict(
            title=dict(
                text=x_label,
                font=dict(
                    size=15,  # Ajusta el tamaño del texto
                    family="Arial",  # Cambia la fuente si lo deseas
                    color="black"  # Opcional: Cambia el color
                )
            ),
            showgrid=True,
            gridcolor='lightgrey'
        ),
        
        yaxis=dict(title=y_label, showgrid=True, gridcolor='lightgrey'),
        template='plotly_white',
        # hovermode='x unified',
        legend=dict(title="Legend", orientation="h", yanchor="bottom", x=0.5, xanchor="center"),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    # fig.update_traces(hovertemplate=f"<b>{x_label}:</b> {{x}}<br><b>{y_label}:</b> {{y}}<extra></extra>")
    
    # offline.plot(fig)
    
    return fig
    
    
