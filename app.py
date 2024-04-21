from dash import Dash, html, dcc, Input, Output, callback, ctx
from datetime import datetime, date, timedelta
import os
from charts import create_elec_prod_bar_chart, create_elec_prod_line_chart, create_elec_prod_pie_chart

app = Dash(__name__)
server = app.server
app.title = 'Energy Production in Switzerland'

today = date.today()
seven_days_ago = today - timedelta(days=7)

def serve_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False, href='/bar'),
        html.Div([
            html.H1('Energy Production in Switzerland', style={'textAlign': 'center'}),
            dcc.Link('Line Chart', href='/elec-prod-line'),
            html.Br(),
            dcc.Link('Bar Chart', href='/elec-prod-bar'),
            html.Br(),
            dcc.Link('Pie Chart', href='/elec-prod-pie'),
        ]),
        html.Div([
            html.Label('Select Start Date:'),
            dcc.DatePickerSingle(
                id='start-date-picker',
                min_date_allowed=datetime(2020, 1, 1),
                max_date_allowed=datetime.today(),
                initial_visible_month=datetime.today(),
                date=seven_days_ago,
                display_format='DD.MM.YYYY'
            ),
            html.Label('Select End Date:'),
            dcc.DatePickerSingle(
                id='end-date-picker',
                min_date_allowed=datetime(2020, 1, 1),
                max_date_allowed=datetime.today(),
                initial_visible_month=datetime.today(),
                date=today,
                display_format='DD.MM.YYYY'
            )
        ], style={'padding': 10}),
        html.Div(id='page-content')
    ])

app.layout = serve_layout

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'), Input('start-date-picker', 'date'), Input('end-date-picker', 'date')])
def display_page(pathname, start_date, end_date):
    if pathname == '/elec-prod-line':
        return create_elec_prod_line_chart(start_date, end_date)
    elif pathname == '/elec-prod-bar':
        return create_elec_prod_bar_chart(start_date, end_date)
    elif pathname == '/elec-prod-pie':
        return create_elec_prod_pie_chart(start_date, end_date)
    else:
        return create_elec_prod_bar_chart(start_date, end_date)
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
