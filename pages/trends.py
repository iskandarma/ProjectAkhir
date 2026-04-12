import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from src.data.load_data import get_data
from src.components.charts import line_chart

dash.register_page(__name__, path="/trends")

df = get_data()

layout = html.Div([
    html.H1("Analisis Tren"),

    dcc.Dropdown(
        id='trend-dropdown',
        options=[{'label': c, 'value': c} for c in df['Cause'].unique()],
        value=df['Cause'].unique()[0]
    ),

    dcc.Graph(id='trend-graph')
])

@dash.callback(
    Output('trend-graph', 'figure'),
    Input('trend-dropdown', 'value')
)
def update_trend(cause):
    return line_chart(df, cause)