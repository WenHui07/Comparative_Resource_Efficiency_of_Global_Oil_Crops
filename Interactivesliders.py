import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Sample Data
data = {
    "Vegetable Oil": ["Palm Oil", "Soybean Oil", "Rapeseed Oil", "Sunflower Oil", "Groundnut Oil", "Cottonseed Oil"],
    "Global Oil Production (Mt)": [78.229, 68.69, 33.776, 20.384, 6.286, 4.76],
    "Oilseed Yield (Mt/ha)": [0.75, 2.87, 2.01, 1.85, 1.75, 1.39],
    "Area Harvested (Million ha)": [27.381, 146.54, 42.428, 28.127, 29.028, 30.209],
    "Land Use (Mha/Mt)": [0.7424, 2.8701, 2.0091, 1.8484, 1.7465, 1.3897],
    "Water Footprint (m3/tonne)": [5000, 4200, 4300, 6800, 7500, 3800],
    "Fertilizer Input (kg/ha/year)": [337.83, 81.94, 126.41, 82.21, 8.67, 184.29],
    "Labour Demand (hrs/ha/year)": [200, 10, 10, 10, 100, 150],
    "Labour Cost ($/tone)": [150, 50, 100, 200, 650, 300]
}

df = pd.DataFrame(data)

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Vegetable Oil Sustainability Dashboard"),

    html.Div([
        html.Label("Max Water Footprint (m3/tonne)"),
        dcc.Slider(
            id='water-slider',
            min=0,
            max=8000,
            step=100,
            value=8000,
            marks={i: str(i) for i in range(0, 8001, 1000)}
        ),
    ], style={'margin': '20px'}),

    html.Div([
        html.Label("Max Fertilizer Input (kg/ha/year)"),
        dcc.Slider(
            id='fertilizer-slider',
            min=0,
            max=400,
            step=10,
            value=400,
            marks={i: str(i) for i in range(0, 401, 50)}
        ),
    ], style={'margin': '20px'}),

    html.Div([
        html.Label("Max Labour (hrs/ha/year)"),
        dcc.Slider(
            id='labour-slider',
            min=0,
            max=300,
            step=10,
            value=300,
            marks={i: str(i) for i in range(0, 301, 50)}
        ),
    ], style={'margin': '20px'}),

    html.Div([
        html.Label("Max Land Use (ha/Mt)"),
        dcc.Slider(
            id='landuse-slider',
            min=0,
            max=4,
            step=0.1,
            value=4,
            marks={i: str(round(i, 1)) for i in range(0, 5)}
        ),
    ], style={'margin': '20px'}),

    dcc.Graph(id="graph-global-production"),
    dcc.Graph(id="graph-yield"),
])

# Callback
@app.callback(
    [dash.dependencies.Output("graph-global-production", "figure"),
     dash.dependencies.Output("graph-yield", "figure")],
    [dash.dependencies.Input("water-slider", "value"),
     dash.dependencies.Input("fertilizer-slider", "value"),
     dash.dependencies.Input("labour-slider", "value"),
     dash.dependencies.Input("landuse-slider", "value")]
)
def update_graphs(water_val, fertilizer_val, labour_val, landuse_val):
    filtered_df = df[
        (df["Water Footprint (m3/tonne)"] <= water_val) &
        (df["Fertilizer Input (kg/ha/year)"] <= fertilizer_val) &
        (df["Labour Demand (hrs/ha/year)"] <= labour_val) &
        (df["Land Use (Mha/Mt)"] <= landuse_val)
    ]

    fig1 = px.bar(filtered_df, x="Vegetable Oil", y="Global Oil Production (Mt)", color="Vegetable Oil",
                    title="Global Production after Filtering")
    fig2 = px.bar(filtered_df, x="Vegetable Oil", y="Oilseed Yield (Mt/ha)", color="Vegetable Oil",
                    title="Yield after Filtering")

    return fig1, fig2

# Run the server
if __name__ == '__main__':
    app.run(debug=True)