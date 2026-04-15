import dash
from dash import html, dcc, Input, Output, callback, dash_table

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

    html.Label('Select Columns to Display'),
    html.Div([
        dcc.Checklist(
            id='column_selector',
            inline=True
        ),
    ], className='column-selector-container'),

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
        page_size= 10,
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

# Callback 1: Update column selector options based on selected dataset
@callback(
    Output('column_selector', 'options'),
    Output('column_selector', 'value'),
    Input('dataset_type', 'value')
)
def update_column_options(dataset_type):
    df = load_data(dataset_type)
    if df.empty:
        return [], []
    
    options = [{'label': i, 'value': i} for i in df.columns]
    
    # Column defaults: hour_studied, attendance, exam_score, academic_status
    # Map them to the actual column names in the CSV
    column_defaults = ["Hours_Studied", "Attendance", "Exam_Score", "Academic_Status"]
    
    # Filter only those that exist in the current dataframe
    default_values = [i for i in column_defaults if i in df.columns]
    
    # If none of the defaults are found, fallback to all columns
    # jika kolom default tidak ditemukan, maka akan menampilkan semua kolom
    if not default_values:
        default_values = [i for i in df.columns]
        
    return options, default_values

# Callback 2: Update table data and columns based on selection
@callback(
    Output('tbl', 'data'),
    Output('tbl', 'columns'),
    Output('tbl_out', 'children'),
    Input('tbl', 'active_cell'),
    Input('dataset_type', 'value'),
    Input('column_selector', 'value')
)
def update_table(active_cell, dataset_type, selected_columns):
    df = load_data(dataset_type)
    
    if df.empty:
        return [], [], "Data tidak ditemukan"
    
    # Filter columns based on user selection
    # If selected_columns is None or empty, return empty data but keep it responsive
    if not selected_columns:
        return [], [], f"{dataset_type} | Silakan pilih kolom pada checkbox di atas"

    # Ensure selected columns actually exist in the current dataframe
    valid_cols = [c for c in selected_columns if c in df.columns]
    
    if not valid_cols:
         return [], [], f"{dataset_type} | Tidak ada kolom yang valid dipilih"

    # Memastikan data dan kolom selalu sinkron
    data = df[valid_cols].to_dict('records')
    columns = [{"name": i, "id": i} for i in valid_cols]
    
    info = "Klik sel pada tabel untuk melihat detailnya"
    if active_cell:
        row = active_cell['row']
        col = active_cell['column_id']
        # Check if clicked column is still visible
        if col in valid_cols:
            try:
                value = df.iloc[row][col]
                info = f"Row {row}, Column '{col}': {value}"
            except (IndexError, KeyError):
                # Handle cases where row might be out of sync
                info = "Data sel tidak tersedia (sinkronisasi tabel...)"
        else:
            info = "Kolom yang diklik tidak lagi terlihat"

    return data, columns, f"{dataset_type} | {info}"