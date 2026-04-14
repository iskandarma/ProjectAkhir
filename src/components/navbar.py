from dash import html, dcc

def Topbar():
    nav_links = [
        {"label": "Home",           "href": "/"},
        {"label": "Dataset",        "href": "/dataset"},
        {"label": "EDA",            "href": "/eda"},
        {"label": "Prediction",     "href": "/prediction"},
        {"label": "Classification", "href": "/classification"},
    ]
    return html.Div([
        html.Span("Student Dashboard", className="topbar-brand"),
        html.Div([
            dcc.Link(item["label"], href=item["href"], className="topbar-link")
            for item in nav_links
        ], className="topbar-nav"),
    ], className="topbar")