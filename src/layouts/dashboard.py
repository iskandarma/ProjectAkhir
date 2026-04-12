from dash import html, dcc
from src.components.navbar import Navbar
from src.components.filters import DropdownCause
from src.data.load_data import get_data

df = get_data()

layout = html.Div([
    Navbar(),

    html.Div([
        html.Label("Pilih Penyebab:"),
        DropdownCause(df)
    ]),

    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart')
], className="container")