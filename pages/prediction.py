import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd

dash.register_page(__name__, path="/prediction", name="Prediction Page")

# Model Coefficients from Prediksi.ipynb
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

def input_wrapper(label, component):
    return html.Div([
        html.Label(label, className="prediction-label"),
        component
    ], style={'marginBottom': '5px'})

layout = html.Div([
    html.Div([
        html.H1("Student Performance Prediction", style={'marginBottom': '5px'}),
        html.P("Real-time exam score calculation based on academic and lifestyle factors.", style={'color': '#7f8c8d'})
    ], style={'marginBottom': '20px'}),
    
    # Input Area (Horizontal Grid)
    html.Div([
        # Row 1: Academic
        html.Div([
            html.Div([
                input_wrapper("Hours Studied", dcc.Input(id="pred-hours", type="number", value=0, min=0, max=168, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Attendance (%)", dcc.Input(id="pred-attendance", type="number", value=0, min=0, max=100, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Prev. Scores", dcc.Input(id="pred-prev-scores", type="number", value=0, min=0, max=100, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Tutoring", dcc.Input(id="pred-tutoring", type="number", value=0, min=0, max=100, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Physical Act.", dcc.Input(id="pred-physical", type="number", value=0, min=0, max=100, className="input-style")),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 -10px', 'marginBottom': '10px'}),
        
        # Row 2: Lifestyle & Environment
        html.Div([
            html.Div([
                input_wrapper("Extracurricular", dcc.Dropdown(
                    id="pred-extracurricular",
                    options=[{'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}],
                    value='Yes', clearable=False
                )),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Internet", dcc.Dropdown(
                    id="pred-internet",
                    options=[{'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}],
                    value='Yes', clearable=False
                )),
            ], style={'flex': '1', 'minWidth': '150px', 'padding': '0 10px'}),
            html.Div([
                input_wrapper("Peer Influence", dcc.Dropdown(
                    id="pred-peer",
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
                    id="pred-parental",
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
                    id="pred-distance",
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
            html.H2("PREDICTED EXAM SCORE", style={'fontSize': '1.2rem', 'margin': '0', 'letterSpacing': '2px', 'color': '#7f8c8d'}),
            html.Div(id="prediction-output", style={
                'fontSize': '80px', 
                'fontWeight': '900', 
                'color': '#2c3e50',
                'lineHeight': '1'
            }),
            html.Div([
                html.Span("Rata-rata kesalahan model (MAE): +-0.98 ")
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
    Output("prediction-output", "children"),
    Input("pred-hours", "value"),
    Input("pred-attendance", "value"),
    Input("pred-prev-scores", "value"),
    Input("pred-tutoring", "value"),
    Input("pred-physical", "value"),
    Input("pred-extracurricular", "value"),
    Input("pred-internet", "value"),
    Input("pred-peer", "value"),
    Input("pred-parental", "value"),
    Input("pred-distance", "value")
)
def update_prediction(hours, attendance, prev_scores, tutoring, physical, 
                      extra, internet, peer, parental, distance):
    # Fallback for None values
    hours = hours or 0
    attendance = attendance or 0
    prev_scores = prev_scores or 0
    tutoring = tutoring or 0
    physical = physical or 0
    
    # Calculate score
    score = COEFS["Intercept"]
    
    # Continuous
    score += COEFS["Hours_Studied"] * hours
    score += COEFS["Attendance"] * attendance
    score += COEFS["Previous_Scores"] * prev_scores
    score += COEFS["Tutoring_Sessions"] * tutoring
    score += COEFS["Physical_Activity"] * physical
    
    # Categorical (Binary)
    if extra == 'Yes':
        score += COEFS["Extracurricular_Activities_Yes"]
    if internet == 'Yes':
        score += COEFS["Internet_Access_Yes"]
        
    # Categorical (One-Hot)
    if peer == 'Positive':
        score += COEFS["Peer_Influence_Positive"]
    elif peer == 'Neutral':
        score += COEFS["Peer_Influence_Neutral"]
        
    if parental == 'Postgraduate':
        score += COEFS["Parental_Education_Level_Postgraduate"]
    elif parental == 'High School':
        score += COEFS["Parental_Education_Level_High School"]
        
    if distance == 'Near':
        score += COEFS["Distance_from_Home_Near"]
    elif distance == 'Moderate':
        score += COEFS["Distance_from_Home_Moderate"]
        
    # Bound score between 0 and 100
    final_score = max(0, min(100, score))
    
    return f"{final_score:.2f}"
