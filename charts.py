import plotly.express as px
from dash import dcc
from data import get_public_power

import plotly.express as px

color_map = {
        'Nuclear': '#EF553B',
        'Hydro Run-of-River': '#19D3F3',
        'Hydro water reservoir': '#AB63FA',
        'Hydro pumped storage': '#636EFA',
        'Wind onshore': '#00CC96',
        'Solar': '#FFA15A'
}

def create_elec_prod_bar_chart(start_date, end_date):
    df = get_public_power(start_date, end_date, ['Nuclear', 'Hydro Run-of-River', 'Hydro water reservoir', 'Hydro pumped storage', 'Wind onshore', 'Solar'])
    fig = px.histogram(df, x='Time', y='Power (MW)', color='Production Type',
                       color_discrete_map=color_map,
                       labels={'Time': 'Time of Day', 'Power (MW)': 'Power in MW'},
                       title='Bar Chart: Energy Production Types Over Time')
    return dcc.Graph(figure=fig, style={'width': '100%'})


def create_elec_prod_line_chart(start_date, end_date):
    df = get_public_power(start_date, end_date, ['Nuclear', 'Hydro Run-of-River', 'Hydro water reservoir', 'Hydro pumped storage', 'Wind', 'Solar'])
    fig = px.line(df, x='Time', y='Power (MW)', color='Production Type',
        color_discrete_map=color_map,
                  labels={'Time': 'Time of Day', 'Power (MW)': 'Power in MW'},
                  title='Line Chart: Energy Production Types Over Time')
    return dcc.Graph(figure=fig,  style={'width': '100%'})

def create_elec_prod_pie_chart(start_date, end_date):
    df = get_public_power(start_date, end_date, ['Nuclear', 'Hydro Run-of-River', 'Hydro water reservoir', 'Hydro pumped storage', 'Wind', 'Solar'])
    df = df[df['Production Type'] != 'Load']
    df_sum = df.groupby('Production Type')['Power (MW)'].sum().reset_index()
    fig = px.pie(df_sum, values='Power (MW)', names='Production Type',
        color_discrete_map=color_map,
                 title='Pie Chart: Total Energy Production by Type',
                 labels={'Production Type': 'Production Type', 'Power (MW)': 'Total Power in MW'})
    return dcc.Graph(figure=fig,  style={'width': '100%'})

def create_elec_prod_heatmap(start_date, end_date):
    df = get_public_power(start_date, end_date, ['Nuclear', 'Hydro Run-of-River', 'Hydro water reservoir', 'Hydro pumped storage', 'Wind', 'Solar'])

    heatmap_data = df.pivot_table(index='Production Type', columns='Time', values='Power (MW)', aggfunc='sum')

    fig = px.imshow(heatmap_data,
                    labels=dict(x="Time of Day", y="Production Type", color="Power in MW"),
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    title="Heatmap: Energy Production Intensity Over Time",
                    aspect="auto")

    fig.update_xaxes(side="top")
    fig.update_layout(xaxis_nticks=20)

    return dcc.Graph(figure=fig, style={'width': '100%'})
