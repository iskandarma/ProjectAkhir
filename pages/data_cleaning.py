import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from src.data.load_data import get_data
from src.components.charts import line_chart

dash.register_page(__name__, path="/data_cleaning", name="Trend Analysis")

df = get_data()

layout = html.Div([
    html.H1("Analisis Tren per Jam Belajar"),

    html.Label("Pilih Status Akademik:"),
    dcc.Dropdown(
        id='trend-dropdown',
        options=[{'label': c, 'value': c} for c in df['Academic_Status'].unique()],
        value=df['Academic_Status'].unique()[0]
    ),

    dcc.Graph(id='trend-graph')
])

@dash.callback(
    Output('trend-graph', 'figure'),
    Input('trend-dropdown', 'value')
)
def update_trend(status):
    return line_chart(df, status)