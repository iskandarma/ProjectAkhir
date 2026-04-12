import plotly.express as px

def line_chart(df, cause):
    dff = df[df['Cause'] == cause]
    fig = px.line(dff, x='Year', y='Total Deaths', title=f'Tren {cause}')
    return fig

def bar_top10(df):
    top = df.groupby('Cause')['Total Deaths'].sum().nlargest(10).reset_index()
    fig = px.bar(top, x='Cause', y='Total Deaths', title='Top 10 Penyebab Kematian')
    return fig

def pie_chart(df, year):
    dff = df[df['Year'] == year]
    fig = px.pie(dff, names='Cause', values='Total Deaths', title=f'Distribusi Tahun {year}')
    return fig