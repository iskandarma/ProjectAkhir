from dash import dcc

def DropdownCause(df):
    return dcc.Dropdown(
        id='cause-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(df['Cause'].unique())],
        value=df['Cause'].unique()[0],
        clearable=False
    )