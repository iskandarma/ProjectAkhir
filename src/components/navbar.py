from dash import html, dcc
import dash

def Navbar():
    return html.Div([
        html.H2("📊 Dashboard Kematian Indonesia"),

        html.Div([
            dcc.Link("Home", href="/"),
            html.Span(" | "),
            dcc.Link("Dataset", href="/dataset"),
            html.Span(" | "),
            dcc.Link("Tren", href="/trends"),
            html.Span(" | "),
            dcc.Link("Perbandingan", href="/comparison"),
        ])
    ])