import pandas as pd

def clean_data(df):
    df = df[['Cause', 'Year', 'Total Deaths']].dropna()
    df['Year'] = df['Year'].astype(int)
    df['Total Deaths'] = df['Total Deaths'].astype(int)
    return df