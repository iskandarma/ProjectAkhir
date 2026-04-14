import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import joblib
import os
import numpy as np

dash.register_page(__name__, path="/classification", name="Classification Page")

# Load Model, Scaler, and Feature Names
MODEL_DIR = "/Users/iskandar/Development/BelajarPython/ProjectAkhir/data/models"
model = joblib.load(os.path.join(MODEL_DIR, "model_classification.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))

def input_wrapper(label, component):
    return html.Div([
        html.Label(label, className="prediction-label"),
        component
    ], style={'marginBottom': '5px'})

layout = html.Div([
    html.Div([
        html.H1("Student Academic Classification", style={'marginBottom': '5px'}),
        html.P("Predict the student's academic status category (Pass, Remidial, or Fail).", style={'color': '#7f8c8d'})
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
    
    # Result Area (Below)
    html.Div([
        html.Div([
            html.H2("ACADEMIC STATUS PREDICTION", style={'fontSize': '1.2rem', 'margin': '0', 'letterSpacing': '2px', 'color': '#7f8c8d'}),
            html.Div(id="classification-output", style={
                'fontSize': '80px', 
                'fontWeight': '900', 
                'lineHeight': '1',
                'margin': '10px 0'
            }),
            html.Div([
                html.Span("Model: Logistic Regression (Multinomial)"),
                html.Br(),
                html.Span("Error Rate: +-25.62% (Global)")
            ], style={'color': '#95a5a6', 'fontSize': '0.9rem', 'marginTop': '10px'})
        ], style={'textAlign': 'center'})
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
     Output("classification-output", "style")],
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
def update_classification(hours, attendance, prev_scores, tutoring, physical, 
                          extra, internet, peer, parental, distance):
    # Prepare input data
    input_data = {
        "Hours_Studied": [hours or 0],
        "Attendance": [attendance or 0],
        "Previous_Scores": [prev_scores or 0],
        "Tutoring_Sessions": [tutoring or 0],
        "Physical_Activity": [physical or 0],
        "Extracurricular_Activities_Yes": [1 if extra == "Yes" else 0],
        "Internet_Access_Yes": [1 if internet == "Yes" else 0],
        "Peer_Influence_Neutral": [1 if peer == "Neutral" else 0],
        "Peer_Influence_Positive": [1 if peer == "Positive" else 0],
        "Parental_Education_Level_High School": [1 if parental == "High School" else 0],
        "Parental_Education_Level_Postgraduate": [1 if parental == "Postgraduate" else 0],
        "Distance_from_Home_Moderate": [1 if distance == "Moderate" else 0],
        "Distance_from_Home_Near": [1 if distance == "Near" else 0]
    }
    
    # Create DataFrame and ensure column order
    input_df = pd.DataFrame(input_data)
    input_df = input_df[feature_names]
    
    # Scale
    X_scaled = scaler.transform(input_df)
    
    # Predict
    pred_idx = model.predict(X_scaled)[0]
    
    # Map index to label
    label_map = {0: "Fail", 1: "Remidial", 2: "Pass"}
    result = label_map[pred_idx]
    
    # Style colors
    colors = {"Pass": "#27ae60", "Remidial": "#f39c12", "Fail": "#e74c3c"}
    
    style = {
        'fontSize': '80px', 
        'fontWeight': '900', 
        'lineHeight': '1',
        'margin': '10px 0',
        'color': colors.get(result, "#2c3e50")
    }
    
    return result.upper(), style
