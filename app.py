from dash import Dash, html, page_container
import dash_bootstrap_components as dbc


from src.components.navbar import Navbar

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    # Navigation
    Navbar(),
    page_container  # ⬅ tempat render halaman
])

if __name__ == "__main__":
    app.run(debug=True)