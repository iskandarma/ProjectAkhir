import dash
from dash import html, dcc
import plotly.express as px
from src.data.load_data import get_data

dash.register_page(__name__, path="/")

df = get_data()

# KPI
total_students = len(df)
avg_score = round(df["Exam_Score"].mean(), 2)
pass_rate = round((df["Academic_Status"] == "Pass").mean() * 100, 2)

# Chart
hist_fig = px.histogram(df, x="Exam_Score", nbins=20)
pie_fig = px.pie(df, names="Academic_Status")

def card(title, value):
    return html.Div([
        html.H4(title, style={'color': '#495057', 'marginBottom': '5px'}),
        html.H2(value, style={'color': '#212529', 'fontWeight': 'bold'})
    ], style={
        'padding': '20px',
        'borderRadius': '12px',
        'backgroundColor': '#ecf0f1',
        'flex': '1',
        'textAlign': 'center',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
    })

layout = html.Div([

    html.H1("Home"),

    # KPI
    html.Div([
        card("Total Data", total_students),
        card("Avg Score", avg_score),
        card("Pass Rate", f"{pass_rate}%"),
    ], style={'display': 'flex', 'gap': '20px', 'width': '100%'}),

    html.Br(),

    # Charts
    html.Div([
        dcc.Graph(figure=hist_fig, style={'flex': '3'}),
        dcc.Graph(figure=pie_fig, style={'flex': '2'}),
    ], style={
        'display': 'flex', 
        'backgroundColor': 'white', 
        'padding': '20px', 
        'borderRadius': '12px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.08)',
        'width': '100%'
    })

])