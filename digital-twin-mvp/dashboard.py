import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import os

# Paths to CSV files generated earlier
TELEMETRY_CSV = "/Users/ahmedmajid/Desktop/Digital-Twin-for Smart-Energy-Meters/digital-twin-mvp/data/telemetry.csv"
EDGE_CSV = "/Users/ahmedmajid/Desktop/Digital-Twin-for Smart-Energy-Meters/digital-twin-mvp/edge_health.csv"

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Digital Twin Dashboard for Smart Energy Meter", style={"text-align": "center"}),

    dcc.Interval(
        id="update-interval",
        interval=10000,   # refresh every 3 seconds
        n_intervals=0
    ),

    html.Div([
        dcc.Graph(id="live-temperature"),
        dcc.Graph(id="live-vibration"),
        dcc.Graph(id="live-pressure"),
        dcc.Graph(id="live-mhi")
    ])
])


@app.callback(
    [
        Output("live-temperature", "figure"),
        Output("live-vibration", "figure"),
        Output("live-pressure", "figure"),
        Output("live-mhi", "figure")
    ],
    [Input("update-interval", "n_intervals")]
)
def update_graphs(n):
    
    if not os.path.exists(TELEMETRY_CSV) or not os.path.exists(EDGE_CSV):
        return {}, {}, {}, {}

    df = pd.read_csv(TELEMETRY_CSV)
    edge = pd.read_csv(EDGE_CSV)

    # Convert timestamps
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    if "timestamp" in edge.columns:
        edge["timestamp"] = pd.to_datetime(edge["timestamp"])

    # === Temperature Chart ===
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["temperature"],
        mode="lines+markers",
        name="Temperature"
    ))
    fig_temp.update_layout(title="Temperature Over Time", xaxis_title="Time", yaxis_title="°C")

    # === Vibration Chart ===
    fig_vib = go.Figure()
    fig_vib.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["vibration"],
        mode="lines+markers",
        name="Vibration"
    ))
    fig_vib.update_layout(title="Vibration", xaxis_title="Time", yaxis_title="mm/s")

    # === Pressure Chart ===
    fig_pres = go.Figure()
    fig_pres.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["pressure"],
        mode="lines+markers",
        name="Pressure"
    ))
    fig_pres.update_layout(title="Pressure", xaxis_title="Time", yaxis_title="kPa")

    # === MHI Chart (from edge device) ===
    fig_mhi = go.Figure()
    fig_mhi.add_trace(go.Scatter(
        x=edge["timestamp"],
        y=edge["MHI"],
        mode="lines+markers",
        name="MHI",
        line=dict(color="green")
    ))
    fig_mhi.update_layout(title="Meter Health Index (0–100)", xaxis_title="Time", yaxis_title="Health Score")

    return fig_temp, fig_vib, fig_pres, fig_mhi


if __name__ == "__main__":
    app.run(debug=True, port=8050)