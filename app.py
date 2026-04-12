from dash import Dash
from src.layouts.dashboard import layout
from src.callbacks.callback import register_callbacks

app = Dash(__name__)
app.title = "Death Dashboard"

app.layout = layout

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)