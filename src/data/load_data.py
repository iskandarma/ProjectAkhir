import pandas as pd
from config import DATA_PATH
from src.data.preprocess import clean_data

def get_data():
    df = pd.read_csv(DATA_PATH)
    df = clean_data(df)
    return df