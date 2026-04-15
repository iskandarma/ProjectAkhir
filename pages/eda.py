import dash
from dash import html, dcc, Input, Output, callback
from src.data.load_data import load_data
from src.components.charts import distribution_plot, correlation_heatmap, scatter_plot, pairplot_matrix
from config import DATASETS

dash.register_page(__name__, path="/eda", name="EDA Page")

# Column lists for distribution
num_cols = [
    "Hours_Studied", "Attendance", "Sleep_Hours", 
    "Previous_Scores", "Tutoring_Sessions", "Physical_Activity", "Exam_Score"
]

layout = html.Div([
    html.H1("Exploratory Data Analysis - EDA"),
    
    html.P("Pilih dataset untuk dianalisis:"),
    dcc.Dropdown(
        id='eda_dataset_selector',
        options=[{'label': k, 'value': k} for k in DATASETS.keys()],
        value="Clean Data",
        clearable=False,
        style={'width': '300px', 'marginBottom': '20px'}
    ),

    dcc.Loading(
        id="loading-eda",
        type="circle",
        children=html.Div(id='eda_content_container')
    )
])

@callback(
    Output('eda_content_container', 'children'),
    Input('eda_dataset_selector', 'value')
)
def update_eda_content(dataset_type):
    df = load_data(dataset_type)
    
    if df.empty:
        return html.Div("Data tidak ditemukan.", style={'color': 'red', 'padding': '20px'})

    # Pastikan kolom numerik ada di dataframe yang dipilih
    available_num_cols = [col for col in num_cols if col in df.columns]

    return [
        html.H2("1. Distribusi Faktor-Faktor Utama", style={'marginTop': '40px'}),
        html.P(f"Melihat penyebaran masing-masing faktor numerik pada dataset {dataset_type}."),
        html.Div([
            html.Div([
                dcc.Graph(figure=distribution_plot(df, col))
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
            for col in available_num_cols
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
    ]