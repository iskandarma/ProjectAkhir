from dash.dependencies import Input, Output
from src.data.load_data import get_data
from src.components.charts import line_chart, bar_top10

df = get_data()

def register_callbacks(app):

    @app.callback(
        Output('line-chart', 'figure'),
        Input('cause-dropdown', 'value')
    )
    def update_line(cause):
        return line_chart(df, cause)

    @app.callback(
        Output('bar-chart', 'figure'),
        Input('cause-dropdown', 'value')
    )
    def update_bar(_):
        return bar_top10(df)