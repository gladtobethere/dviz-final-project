from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from api.public_power import get_public_power
import os
import flask

server = flask.Flask(__name__)
app = Dash(__name__, server=server)

app.layout = html.Div([
    html.H1('Energy Production in Switzerland', style={'textAlign': 'center'}),
    dcc.Graph(id='energy-production-chart')
])

@app.callback(
    Output('energy-production-chart', 'figure'),
    Input('energy-production-chart', 'id')
)
def update_graph(_):
    df = get_public_power('2023-01-01T00:00+01:00', '2023-01-01T23:45+01:00')
    fig = px.line(df, x='Time', y='Power (MW)', color='Production Type',
                  labels={'Time': 'Time of Day', 'Power (MW)': 'Power in MW'},
                  title='Energy Production Types Over Time')
    fig.update_xaxes(rangeslider_visible=True)
    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
