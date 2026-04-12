import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from src.data.load_data import get_data
from src.components.charts import bar_top10

dash.register_page(__name__, path="/comparison")

df = get_data()

layout = html.Div([
    html.H1("Perbandingan"),

    dcc.Graph(id='bar-chart')
])

@dash.callback(
    Output('bar-chart', 'figure'),
    Input('bar-chart', 'id')
)
def update_bar(_):
    return bar_top10(df)