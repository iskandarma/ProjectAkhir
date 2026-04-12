import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H1("Home"),
    html.P("Selamat datang di dashboard analisis kematian di Indonesia")
])