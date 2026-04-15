import dash
from dash import html, dcc, Input, Output, callback, dash_table
import pandas as pd

from src.data.load_data import load_data
from config import DATASETS

dash.register_page(__name__, path="/dataset", name="Dataset Page")

layout = html.Div([
    html.Label('Dataset Viewer'),
    
    dcc.Dropdown(
        id='dataset_type',
        options=[{'label': k, 'value': k} for k in DATASETS.keys()],
        value="Raw Data",
        clearable=False
    ),
    
    html.Br(),

    # styling untuk tabel 
    # sumber https://dash.plotly.com/datatable/style
    dash_table.DataTable(
        id='tbl',
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        selected_rows=[],
        page_action='native',
        page_current= 0,
        page_size= 15,
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
            },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
            },
        style_cell_conditional=[
        {
            'if': {'column_id': 'Cause'},
            'textAlign': 'left',
            'minWidth': '400px', 
            'width': '400px', 
            'maxWidth': '400px'
        },
        {
            'if': {'column_id': 'Type'},
            'textAlign': 'left',
            'minWidth': '300px', 
            'width': '300px', 
            'maxWidth': '300px'
        }
        ]),
    
    html.Br(),

    html.Div(
        id='tbl_out',
        className='alert-box'
        )
    ])

# callback khusus halaman ini
@callback(
    Output('tbl', 'data'),
    Output('tbl', 'columns'),
    Output('tbl_out', 'children'),
    Input('tbl', 'active_cell'),
    Input('dataset_type', 'value')
)
def update_graphs(active_cell, dataset_type):
    df = load_data(dataset_type)
    
    if df.empty:
        return [], [], "Data tidak ditemukan"
    
    data = df.to_dict('records')
    columns = [{"name": i, "id": i} for i in df.columns]
    
    if active_cell:
        row = active_cell['row']
        col = active_cell['column_id']
        value = df.iloc[row][col]
        info = f"Row {row}, Column '{col}': {value}"
    else:
        info = "Klik sel pada tabel untuk melihat detailnya"

    return data, columns, f"{dataset_type} | {info}"