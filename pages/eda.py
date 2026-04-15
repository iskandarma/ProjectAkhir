import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from src.data.load_data import get_data
from src.components.charts import distribution_plot, correlation_heatmap, scatter_plot, pairplot_matrix

dash.register_page(__name__, path="/eda", name="EDA Page")

df = get_data()

# Column lists for distribution
num_cols = [
    "Hours_Studied", "Attendance", "Sleep_Hours", 
    "Previous_Scores", "Tutoring_Sessions", "Physical_Activity", "Exam_Score"
]

layout = html.Div([
    html.H1("Exploratory Data Analysis"),
    
    html.H2("1. Distribusi Faktor-Faktor Utama", style={'marginTop': '40px'}),
    html.P("Melihat penyebaran masing-masing faktor numerik."),
    html.Div([
        html.Div([
            dcc.Graph(figure=distribution_plot(df, col))
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
        for col in num_cols
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}),

    html.H2("2. Korelasi Antar Faktor", style={'marginTop': '40px'}),
    html.P("Mengidentifikasi hubungan linear antar variabel numerik."),
    dcc.Graph(figure=correlation_heatmap(df)),

    html.H2("3. Matriks Hubungan (Pairplot)", style={'marginTop': '40px'}),
    html.P("Visualisasi hubungan antar beberapa faktor utama secara sekaligus."),
    dcc.Graph(figure=pairplot_matrix(df)),

    html.H2("4. Detail Hubungan: Jam Belajar vs Skor Ujian", style={'marginTop': '40px'}),
    html.P("Melihat secara spesifik bagaimana jam belajar mempengaruhi skor ujian."),
    dcc.Graph(figure=scatter_plot(df, "Hours_Studied", "Exam_Score"))
])