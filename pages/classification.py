import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import joblib
import os
import numpy as np
import random
from config import MODEL_DIR

dash.register_page(__name__, path="/classification", name="Classification Page")

# Load Model, Scaler, and Feature Names
model = joblib.load(os.path.join(MODEL_DIR, "model_classification.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))

# Model Coefficients from Prediksi.ipynb (for Score Prediction)
COEFS = {
    "Intercept": 38.06446787080266,
    "Peer_Influence_Positive": 1.075134,
    "Internet_Access_Yes": 1.002231,
    "Distance_from_Home_Near": 0.941533,
    "Peer_Influence_Neutral": 0.538316,
    "Extracurricular_Activities_Yes": 0.492132,
    "Tutoring_Sessions": 0.484201,
    "Parental_Education_Level_Postgraduate": 0.459020,
    "Distance_from_Home_Moderate": 0.423431,
    "Hours_Studied": 0.292456,
    "Attendance": 0.197459,
    "Physical_Activity": 0.196885,
    "Previous_Scores": 0.048741,
    "Parental_Education_Level_High School": -0.487155
}

# Terjemahan dan Motivasi
LABEL_IDN = {
    "Pass": "Lulus",
    "Remidial": "Mengulang",
    "Remedial": "Mengulang",
    "Fail": "Tidak Lulus"
}

MOTIVATIONS = {
    "Lulus": [
        "Luar biasa! Kamu telah menunjukkan hasil yang gemilang. Pertahankan kerja kerasmu!",
        "Prestasi yang membanggakan! Teruslah konsisten untuk meraih impian yang lebih tinggi.",
        "Selamat! Hasil ini adalah bukti dedikasimu. Masa depan yang cerah menantimu."
    ],
    "Mengulang": [
        "Sedikit lagi! Evaluasi kembali materi yang sulit dan kamu pasti bisa melampauinya.",
        "Jangan menyerah, kamu hanya butuh sedikit perbaikan. Ayo tetap semangat belajar!",
        "Masih ada kesempatan! Fokus pada area yang kurang dan buktikan kamu bisa lebih baik."
    ],
    "Tidak Lulus": [
        "Kegagalan bukanlah akhir. Jadikan ini sebagai pelajaran untuk bangkit lebih kuat.",
        "Tetap semangat! Temukan metode belajar yang lebih efektif dan coba lagi dengan berani.",
        "Setiap tantangan adalah proses pendewasaan. Ayo evaluasi diri dan mulai langkah baru!"
    ]
}

def input_wrapper(label, component):
    return html.Div([
        html.Label(label, className="prediction-label"),
        component
    ], style={'marginBottom': '5px'})

layout = html.Div([
    html.Div([
        html.H1("Student Academic Classification & Score", style={'marginBottom': '5px'}),
        html.P("Predict the student's academic status category and numerical exam score.", style={'color': '#7f8c8d'})
    ], style={'marginBottom': '20px'}),
    
    # Input Area (Horizontal Grid)
    html.Div([
        # Row 1: Academic
        html.Div([
            html.Div([
                input_wrapper("Hours Studied", dcc.Input(id="class-hours", type="number", value=0, min=0, max=168, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Attendance (%)", dcc.Input(id="class-attendance", type="number", value=0, min=0, max=100, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Prev. Scores", dcc.Input(id="class-prev-scores", type="number", value=0, min=0, max=100, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Tutoring", dcc.Input(id="class-tutoring", type="number", value=0, min=0, max=100, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Physical Act.", dcc.Input(id="class-physical", type="number", value=0, min=0, max=100, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 -10px', 'marginBottom': '10px'}),
        
        # Row 2: Lifestyle & Environment
        html.Div([
            html.Div([
                input_wrapper("Extracurricular", dcc.Dropdown(
                    id="class-extracurricular",
                    options=[{'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}],
                    value='Yes', clearable=False
                )),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Internet", dcc.Dropdown(
                    id="class-internet",
                    options=[{'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}],
                    value='Yes', clearable=False
                )),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Peer Influence", dcc.Dropdown(
                    id="class-peer",
                    options=[
                        {'label': 'Positive', 'value': 'Positive'},
                        {'label': 'Neutral', 'value': 'Neutral'},
                        {'label': 'Negative', 'value': 'Negative'}
                    ],
                    value='Neutral', clearable=False
                )),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Parental Edu", dcc.Dropdown(
                    id="class-parental",
                    options=[
                        {'label': 'High School', 'value': 'High School'},
                        {'label': 'College', 'value': 'College'},
                        {'label': 'Postgraduate', 'value': 'Postgraduate'}
                    ],
                    value='College', clearable=False
                )),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Distance", dcc.Dropdown(
                    id="class-distance",
                    options=[
                        {'label': 'Near', 'value': 'Near'},
                        {'label': 'Moderate', 'value': 'Moderate'},
                        {'label': 'Far', 'value': 'Far'}
                    ],
                    value='Moderate', clearable=False
                )),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 -10px'}),
    ], className="form-section", style={'padding': '20px', 'marginBottom': '20px'}),
    
    # Combined Result Area
    html.Div([
        html.Div([
            # Academic Status Column
            html.Div([
                html.H2("ACADEMIC STATUS", style={'fontSize': '1rem', 'margin': '0', 'letterSpacing': '2px', 'color': '#7f8c8d'}),
                html.Div(id="classification-output", style={'fontSize': '45px', 'fontWeight': '900', 'margin': '10px 0'}),
            ], style={'flex': '1', 'borderRight': '1px solid #edf2f7', 'padding': '10px'}),
            
            # Predicted Score Column
            html.Div([
                html.H2("PREDICTED SCORE", style={'fontSize': '1rem', 'margin': '0', 'letterSpacing': '2px', 'color': '#7f8c8d'}),
                html.Div(id="class-prediction-output", style={'fontSize': '45px', 'fontWeight': '900', 'color': '#2c3e50', 'margin': '10px 0'}),
            ], style={'flex': '1', 'padding': '10px'}),
        ], style={'display': 'flex', 'textAlign': 'center'}),
        
        html.Hr(style={'margin': '20px 0', 'border': '0', 'borderTop': '1px solid #edf2f7'}),
        
        html.Div(id="classification-summary", style={
            'fontSize': '1.1rem', 
            'fontStyle': 'italic', 
            'color': '#34495e', 
            'textAlign': 'center',
            'marginBottom': '15px'
        }),

        html.Div([
            html.Span("Models: Logistic Regression (Classification) & Linear Regression (Score Prediction)"),
            html.Br(),
            html.Span("MAE Score: +-0.98 | Error Rate Class: +-25.62%")
        ], style={'color': '#95a5a6', 'fontSize': '0.85rem', 'textAlign': 'center'})
    ], style={
        'padding': '30px',
        'borderRadius': '16px',
        'backgroundColor': 'white',
        'boxShadow': '0 10px 25px rgba(0,0,0,0.05)',
        'border': '1px solid #edf2f7'
    })
], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'})

@callback(
    [Output("classification-output", "children"),
     Output("classification-output", "style"),
     Output("class-prediction-output", "children"),
     Output("classification-summary", "children")],
    [Input("class-hours", "value"),
     Input("class-attendance", "value"),
     Input("class-prev-scores", "value"),
     Input("class-tutoring", "value"),
     Input("class-physical", "value"),
     Input("class-extracurricular", "value"),
     Input("class-internet", "value"),
     Input("class-peer", "value"),
     Input("class-parental", "value"),
     Input("class-distance", "value")]
)
def update_results(hours, attendance, prev_scores, tutoring, physical, 
                   extra, internet, peer, parental, distance):
    # --- Part 1: Numerical Score Prediction (Linear Logic) ---
    val_hours = hours or 0
    val_attendance = attendance or 0
    val_prev_scores = prev_scores or 0
    val_tutoring = tutoring or 0
    val_physical = physical or 0
    
    score = COEFS["Intercept"]
    score += COEFS["Hours_Studied"] * val_hours
    score += COEFS["Attendance"] * val_attendance
    score += COEFS["Previous_Scores"] * val_prev_scores
    score += COEFS["Tutoring_Sessions"] * val_tutoring
    score += COEFS["Physical_Activity"] * val_physical
    
    if extra == 'Yes': score += COEFS["Extracurricular_Activities_Yes"]
    if internet == 'Yes': score += COEFS["Internet_Access_Yes"]
    if peer == 'Positive': score += COEFS["Peer_Influence_Positive"]
    elif peer == 'Neutral': score += COEFS["Peer_Influence_Neutral"]
    if parental == 'Postgraduate': score += COEFS["Parental_Education_Level_Postgraduate"]
    elif parental == 'High School': score += COEFS["Parental_Education_Level_High School"]
    if distance == 'Near': score += COEFS["Distance_from_Home_Near"]
    elif distance == 'Moderate': score += COEFS["Distance_from_Home_Moderate"]
    
    final_score = max(0, min(100, score))
    formatted_score = f"{final_score:.2f}"

    # --- Part 2: Categorical Classification (Logistic Logic) ---
    input_data = {
        "Hours_Studied": [val_hours],
        "Attendance": [val_attendance],
        "Previous_Scores": [val_prev_scores],
        "Tutoring_Sessions": [val_tutoring],
        "Physical_Activity": [val_physical],
        "Extracurricular_Activities_Yes": [1 if extra == "Yes" else 0],
        "Internet_Access_Yes": [1 if internet == "Yes" else 0],
        "Peer_Influence_Neutral": [1 if peer == "Neutral" else 0],
        "Peer_Influence_Positive": [1 if peer == "Positive" else 0],
        "Parental_Education_Level_High School": [1 if parental == "High School" else 0],
        "Parental_Education_Level_Postgraduate": [1 if parental == "Postgraduate" else 0],
        "Distance_from_Home_Moderate": [1 if distance == "Moderate" else 0],
        "Distance_from_Home_Near": [1 if distance == "Near" else 0]
    }
    
    input_df = pd.DataFrame(input_data)
    input_df = input_df[feature_names]
    X_scaled = scaler.transform(input_df)
    pred_idx = model.predict(X_scaled)[0]
    
    label_map_en = {0: "Fail", 1: "Remidial", 2: "Pass"}
    res_en = label_map_en[pred_idx]
    
    # Map to Indonesian
    res_idn = LABEL_IDN.get(res_en, res_en)
    
    colors = {"Pass": "#27ae60", "Remidial": "#f1c40f", "Fail": "#e74c3c"}
    
    status_style = {
        'fontSize': '45px', 
        'fontWeight': '900', 
        'margin': '10px 0',
        'color': colors.get(res_en, "#2c3e50")
    }

    # Motivational Sentence selection
    quotes = MOTIVATIONS.get(res_idn, ["Tetap semangat belajar!"])
    motivation = random.choice(quotes)
    
    summary_text = f"Berdasarkan faktor-faktor di atas, siswa diprediksi {res_idn.upper()} dengan estimasi nilai ujian sebesar {formatted_score}. {motivation}"
    
    return res_en.upper(), status_style, formatted_score, summary_text
