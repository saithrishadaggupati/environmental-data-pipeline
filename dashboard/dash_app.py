import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()

logger.info("Loading data for Dash dashboard")

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    connect_args={"sslmode": "require"}
)

df = pd.read_sql("SELECT * FROM aqi_readings", engine)

latest = df.sort_values("timestamp").groupby("city").last().reset_index()
latest_sorted = latest.sort_values("aqi_index", ascending=False)

cities_tracked = len(latest)
most_polluted = latest.loc[latest['aqi_index'].idxmax(), 'city']
cleanest_city = latest.loc[latest['aqi_index'].idxmin(), 'city']
hazardous_count = len(latest[latest['air_quality_label'] == 'Hazardous'])

color_map = {
    "Good": "#2ecc71",
    "Moderate": "#f39c12",
    "Unhealthy": "#e67e22",
    "Hazardous": "#e74c3c"
}

fig_bar = px.bar(
    latest_sorted,
    x="city", y="aqi_index",
    color="air_quality_label",
    title="AQI Levels Across 25 Indian Cities",
    labels={"aqi_index": "AQI Index", "city": "City"},
    color_discrete_map=color_map
)

category_counts = latest['air_quality_label'].value_counts().reset_index()
category_counts.columns = ['Category', 'Cities']
fig_pie = px.pie(
    category_counts,
    names='Category', values='Cities',
    title='Cities by Air Quality Category',
    color_discrete_map=color_map
)

fig_scatter = px.scatter(
    latest_sorted,
    x="pm2_5", y="aqi_index",
    color="air_quality_label",
    size="aqi_index",
    hover_name="city",
    title="PM2.5 vs AQI Index by City",
    labels={"pm2_5": "PM2.5", "aqi_index": "AQI Index"}
)

app = dash.Dash(__name__)
app.title = "India AQI Dashboard"
server = app.server

card_style = {
    'backgroundColor': 'white',
    'padding': '20px',
    'borderRadius': '10px',
    'textAlign': 'center',
    'width': '20%',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
}

app.layout = html.Div(
    style={'fontFamily': 'Arial', 'backgroundColor': '#f8f9fa', 'padding': '20px'},
    children=[
        html.H1("🌍 India Air Quality Dashboard",
                style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.P("Live data from 25 Indian cities — updated every 6 hours",
               style={'textAlign': 'center', 'color': '#7f8c8d'}),
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px'},
            children=[
                html.Div(style=card_style, children=[
                    html.H3(cities_tracked, style={'color': '#3498db', 'margin': '0'}),
                    html.P("Cities Tracked", style={'color': '#7f8c8d'})
                ]),
                html.Div(style=card_style, children=[
                    html.H3(most_polluted, style={'color': '#e74c3c', 'margin': '0'}),
                    html.P("Most Polluted", style={'color': '#7f8c8d'})
                ]),
                html.Div(style=card_style, children=[
                    html.H3(cleanest_city, style={'color': '#2ecc71', 'margin': '0'}),
                    html.P("Cleanest City", style={'color': '#7f8c8d'})
                ]),
                html.Div(style=card_style, children=[
                    html.H3(hazardous_count, style={'color': '#e67e22', 'margin': '0'}),
                    html.P("Hazardous Cities", style={'color': '#7f8c8d'})
                ]),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'},
            children=[
                html.Div(style={'flex': '2', 'backgroundColor': 'white', 'borderRadius': '10px',
                                'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'},
                         children=[dcc.Graph(figure=fig_bar)]),
                html.Div(style={'flex': '1', 'backgroundColor': 'white', 'borderRadius': '10px',
                                'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'},
                         children=[dcc.Graph(figure=fig_pie)]),
            ]
        ),
        html.Div(
            style={'backgroundColor': 'white', 'borderRadius': '10px',
                   'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginBottom': '20px'},
            children=[dcc.Graph(figure=fig_scatter)]
        ),
        html.H3("Full Data Table", style={'color': '#2c3e50'}),
        dash_table.DataTable(
            data=latest_sorted[["city", "aqi_index", "pm2_5", "pm10", "co", "air_quality_label", "timestamp"]].to_dict('records'),
            columns=[{"name": i, "id": i} for i in ["city", "aqi_index", "pm2_5", "pm10", "co", "air_quality_label", "timestamp"]],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#2c3e50', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'filter_query': '{air_quality_label} = "Hazardous"'}, 'backgroundColor': '#fadbd8'},
                {'if': {'filter_query': '{air_quality_label} = "Good"'}, 'backgroundColor': '#d5f5e3'},
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)