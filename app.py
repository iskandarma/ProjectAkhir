from dash import Dash, html, page_container
import dash_mantine_components as dmc
from src.components.navbar import Topbar

app = Dash(__name__, use_pages=True)

app.layout = dmc.MantineProvider(
    children=[
        Topbar(),
        html.Div(page_container, className="main-content"),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)