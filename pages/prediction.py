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
        html.Label(label, style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
        component
    ], style={'marginBottom': '15px'})

layout = html.Div([
    html.H1("Student Performance Prediction"),
    html.P("Predict the final exam score based on academic and lifestyle factors."),
    
    html.Div([
        # Left Column: Inputs
        html.Div([
            html.Div([
                html.H3("Academic Factors"),
                input_wrapper("Hours Studied (per week)", dcc.Input(id="pred-hours", type="number", value=20, min=0, max=168, className="input-style")),
                input_wrapper("Attendance (%)", dcc.Input(id="pred-attendance", type="number", value=90, min=0, max=100, className="input-style")),
                input_wrapper("Previous Scores (0-100)", dcc.Input(id="pred-prev-scores", type="number", value=75, min=0, max=100, className="input-style")),
                input_wrapper("Tutoring Sessions", dcc.Input(id="pred-tutoring", type="number", value=2, min=0, max=20, className="input-style")),
            ], className="form-section"),
            
            html.Div([
                html.H3("Lifestyle Factors"),
                input_wrapper("Physical Activity (hours/week)", dcc.Input(id="pred-physical", type="number", value=3, min=0, max=20, className="input-style")),
                input_wrapper("Extracurricular Activities", dcc.Dropdown(
                    id="pred-extracurricular",
                    options=[{'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}],
                    value='No',
                    clearable=False
                )),
                input_wrapper("Internet Access", dcc.Dropdown(
                    id="pred-internet",
                    options=[{'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}],
                    value='Yes',
                    clearable=False
                )),
            ], className="form-section"),
            
            html.Div([
                html.H3("Environment Factors"),
                input_wrapper("Peer Influence", dcc.Dropdown(
                    id="pred-peer",
                    options=[
                        {'label': 'Positive', 'value': 'Positive'},
                        {'label': 'Neutral', 'value': 'Neutral'},
                        {'label': 'Negative', 'value': 'Negative'}
                    ],
                    value='Neutral',
                    clearable=False
                )),
                input_wrapper("Parental Education", dcc.Dropdown(
                    id="pred-parental",
                    options=[
                        {'label': 'High School', 'value': 'High School'},
                        {'label': 'College', 'value': 'College'},
                        {'label': 'Postgraduate', 'value': 'Postgraduate'}
                    ],
                    value='College',
                    clearable=False
                )),
                input_wrapper("Distance from Home", dcc.Dropdown(
                    id="pred-distance",
                    options=[
                        {'label': 'Near', 'value': 'Near'},
                        {'label': 'Moderate', 'value': 'Moderate'},
                        {'label': 'Far', 'value': 'Far'}
                    ],
                    value='Moderate',
                    clearable=False
                )),
            ], className="form-section"),
        ], style={'flex': '1', 'marginRight': '20px'}),
        
        # Right Column: Result
        html.Div([
            html.Div([
                html.H2("Prediction Result", style={'textAlign': 'center', 'color': '#2c3e50'}),
                html.Hr(),
                html.Div(id="prediction-output", style={
                    'fontSize': '64px', 
                    'textAlign': 'center', 
                    'fontWeight': 'bold', 
                    'color': '#3498db',
                    'margin': '20px 0'
                }),
                html.P("Predicted Exam Score (0-100)", style={'textAlign': 'center', 'color': '#7f8c8d'}),
                html.Div([
                    html.Strong("Model Info: "),
                    html.Span("Linear Regression (MAE: ±0.98)")
                ], style={'marginTop': '40px', 'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'})
            ], style={
                'position': 'sticky', 
                'top': '20px',
                'padding': '30px',
                'borderRadius': '16px',
                'backgroundColor': 'white',
                'boxShadow': '0 8px 30px rgba(0,0,0,0.1)'
            })
        ], style={'flex': '1'}),
    ], style={'display': 'flex', 'alignItems': 'flex-start'})
], style={'padding': '20px'})

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
