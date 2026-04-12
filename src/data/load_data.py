import pandas as pd
from config import DATA_PATH, DATASETS
from src.data.preprocess import show_data

def get_data():
    df = pd.read_csv(DATA_PATH)
    df = show_data(df)
    return df

def load_data(dataset_type):
    path = DATASETS.get(dataset_type)
    df = pd.read_csv(path)
    df = show_data(df)
    if path:
        return df
    return pd.DataFrame()