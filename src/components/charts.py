import plotly.express as px

def line_chart(df, status):
    dff = df[df['Academic_Status'] == status]
    # Usahakan plot Exam_Score berdasarkan Hours_Studied
    dff = dff.groupby('Hours_Studied')['Exam_Score'].mean().reset_index()
    fig = px.line(dff, x='Hours_Studied', y='Exam_Score', title=f'Rata-rata Skor per Jam Belajar ({status})')
    return fig

def bar_top10(df):
    # Rata-rata Skor berdasarkan Academic_Status
    top = df.groupby('Academic_Status')['Exam_Score'].mean().reset_index()
    fig = px.bar(top, x='Academic_Status', y='Exam_Score', title='Rata-rata Skor Berdasarkan Status Akademik')
    return fig

# Define a consistent color map for academic status
status_colors = {'Pass': '#2ecc71', 'Fail': '#e74c3c', 'Remidial': '#f1c40f'}

def pie_chart(df, gender):
    dff = df[df['Gender'] == gender]
    fig = px.pie(
        dff, names='Academic_Status', 
        title=f'Distribusi Status Akademik ({gender})',
        color='Academic_Status',
        color_discrete_map=status_colors
    )
    return fig

def distribution_plot(df, column):
    fig = px.histogram(
        df, x=column, 
        marginal="box", # Adds a boxplot on top
        title=f'Distribusi {column.replace("_", " ")}',
        template="plotly_white",
        color_discrete_sequence=['#636EFA']
    )
    return fig

def correlation_heatmap(df):
    num_cols = df.select_dtypes(include=['number']).columns
    corr = df[num_cols].corr()
    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Heatmap Korelasi Antar Faktor Numerik",
        color_continuous_scale='RdBu_r'
    )
    return fig

def scatter_plot(df, x_col, y_col):
    fig = px.scatter(
        df, x=x_col, y=y_col,
        title=f'Hubungan {x_col.replace("_", " ")} vs {y_col.replace("_", " ")}',
        template="plotly_white",
        opacity=0.6
    )
    return fig

def pairplot_matrix(df):
    num_cols = [
        "Hours_Studied", "Attendance", "Exam_Score"
    ]
    fig = px.scatter_matrix(
        df,
        dimensions=num_cols,
        color="Academic_Status",
        color_discrete_map=status_colors,
        title="Pairplot (Scatter Matrix) Faktor Utama",
        template="plotly_white",
        opacity=0.4
    )
    # Reduce label size for better fit
    # fig.update_traces(diagonal_visible=False) # Keep diagonal for distribution
    fig.update_layout(height=800)
    return fig