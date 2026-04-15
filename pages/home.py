import dash
from dash import html, dcc
import plotly.express as px
from src.data.load_data import get_data

dash.register_page(__name__, path="/")

df = get_data()

# Menghitung jumlah data
total_students = len(df)
# Menghitung rata-rata nilai
avg_score = round(df["Exam_Score"].mean(), 2)
# Menghitung persentase kelulusan
pass_rate = round((df["Academic_Status"] == "Pass").mean() * 100, 2)

# Membuat chart
hist_fig = px.histogram(df, x="Exam_Score", nbins=20)
pie_fig = px.pie(df, names="Academic_Status", color="Academic_Status",
                 color_discrete_map={'Pass': '#2ecc71', 'Fail': '#e74c3c', 'Remidial': '#f1c40f'})

# Membuat card
def card(title, value):
    return html.Div([
        html.H4(title),
        html.H2(value)
    ], className='kpi-card')

layout = html.Div([

    html.H1("Home"),

    # Menampilkan KPI
    html.Div([
        card("Total Data", total_students),
        card("Avg Score", avg_score),
        card("Pass Rate", f"{pass_rate}%"),
    ], className='kpi-container'),

    html.Br(),

    # Menampilkan chart
    html.Div([
        dcc.Graph(figure=hist_fig, className='graph-large'),
        dcc.Graph(figure=pie_fig, className='graph-small'),
    ], className='chart-container')

])