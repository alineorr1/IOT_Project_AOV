#Libraries
from dash.dependencies import Input, Output
import plotly.express as px
import dash_table
import pandas as pd

#logging config
import logging

# Logger Config
logger = logging.getLogger('myAppLogger')

#%%

def register_callbacks(app, heart_rate_df: pd.DataFrame):
    source_map = {
        "rest": "😴",
        "workout": "🏃",
        "awake": "📚",
    }

    @app.callback(
        Output("heart-rate-graph", "figure"),
        Input("heart-rate-graph", "hoverData")
    )
    def update_graph(hover_data):
        heart_rate_df["bpm"] = heart_rate_df["bpm"].round(2)
        
        heart_rate_df["emoji"] = heart_rate_df["source"].map(source_map)
        
        fig = px.line(
            heart_rate_df,
            x="timestamp",
            y="bpm",
            color="source",
            line_group="source",
            hover_data={"emoji": True, "bpm": True, "source": True},
            title="Heart Rate with Activity Source"
        )
        fig.update_traces(mode="markers+lines", marker=dict(size=6))
        fig.update_layout(
            width=900,
            height=700
        )
        return fig

    @app.callback(
        Output("hover-info", "children"),
        Input("heart-rate-graph", "hoverData")
    )
    def update_hover_info(hover_data):
        if hover_data is None:
            return "Hover over a point to see details."
        
        point = hover_data["points"][0]
        timestamp = point["x"]
        bpm = point["y"]
        source = point["customdata"][0]
        emoji = source_map.get(source, "Oura Ring")

        return f"Timestamp: {timestamp}, BPM: {bpm}, Source: {source} {emoji}"

    @app.callback(
        Output("activity-table-container", "children"),
        Input("heart-rate-graph", "selectedData")
    )
    def update_table(selected_data):
        if selected_data is None:
            return "Select a range in the graph to explore data."

        selected_points = [point["x"] for point in selected_data["points"]]
        filtered_df = heart_rate_df[heart_rate_df["timestamp"].isin(selected_points)]

        return dash_table.DataTable(
            data=filtered_df.to_dict("records"),
            columns=[{"name": col, "id": col} for col in filtered_df.columns],
            style_cell={"textAlign": "center", "fontFamily": "Arial"},
            style_header={"fontWeight": "bold", "backgroundColor": "rgb(230, 230, 230)"},
            style_table={"overflowX": "auto"},
        )
    
    @app.callback(
        Output("heart-rate-df-container", "children"),
        Input("heart-rate-graph", "id")
    )
    def update_heart_rate_table(_):
        return dash_table.DataTable(
            id="heart-rate-df-table",
            columns=[{"name": col, "id": col} for col in heart_rate_df.columns],
            data=heart_rate_df.to_dict("records"),
            style_table={"height": "1000", "overflowY": "auto", "marginTop": "10px"},
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
                "textAlign": "center"
            },
            style_cell={
                "textAlign": "center",
                "fontFamily": "Arial",
                "padding": "10px",
                "fontSize": "12px"
            },
            fixed_rows={"headers": True}
        )        
