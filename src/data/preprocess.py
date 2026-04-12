import pandas as pd

def show_data(df):
    df = df[['Cause', 'Type', 'Data Redundancy', 'Year', 'Total Deaths']].dropna()
    df['Cause'] = df['Cause'].astype(str)
    df['Type'] = df['Type'].astype(str)
    df['Data Redundancy'] = df['Data Redundancy'].astype(int)
    df['Year'] = df['Year'].astype(int)
    df['Total Deaths'] = df['Total Deaths'].astype(int)
    return df