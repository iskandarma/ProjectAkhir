import pandas as pd

def show_data(df):
    # Select a subset of useful columns for the dashboard
    cols = [
        'Hours_Studied', 'Attendance', 'Parental_Involvement', 
        'Access_to_Resources', 'Extracurricular_Activities', 
        'Sleep_Hours', 'Previous_Scores', 'Motivation_Level', 
        'Internet_Access', 'Tutoring_Sessions', 'Family_Income', 
        'Teacher_Quality', 'School_Type', 'Peer_Influence', 
        'Physical_Activity', 'Learning_Disabilities', 
        'Parental_Education_Level', 'Distance_from_Home', 
        'Gender', 'Exam_Score', 'Academic_Status'
    ]
    # Filter to only existing columns just in case
    existing_cols = [c for c in cols if c in df.columns]
    df = df[existing_cols].dropna()
    
    # Ensure types are correct
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
    
    return df