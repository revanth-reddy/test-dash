import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import psycopg2
from datetime import datetime as dt


app = dash.Dash()
# app.title = 'WC'

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>WC</title>
        <link rel="shortcut icon" type="image/png" href="https://media.licdn.com/dms/image/C510BAQEURkOFeoSlKA/company-logo_200_200/0?e=2159024400&v=beta&t=XBXB_eFyHDN0Rf5ZGc3X1R9nHY1VBqTuY_vBU3jUOfA"/>
        {%css%}
    </head>
    <body>
        <!-- <div>My Custom header</div> -->
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div>My Custom footer</div>
    </body>
</html>
'''
conn = psycopg2.connect(host="john.db.elephantsql.com",database="hibzxjxl", user="hibzxjxl", password="BbJmB-QJQegz1z8f4jmsfsUY0GsNXehi")

cur = conn.cursor()
cur.execute("SELECT * from timetrend")
# print("The number of parts: ", cur.rowcount)
row = cur.fetchone()
time=[]
cov=[]
while row is not None:
            # print(row)
            time.append(row[0])
            cov.append(row[1])
            row = cur.fetchone()
# print(n)
cur.close()

dtmin = min(time)
dtmax = max(time)

app.layout = html.Div([
    dcc.Link(html.H3('Home'),style={'text-decoration': 'none'}, href = '/'),
    dcc.Graph(id = 'livegraph', style={'width':'100%',}),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        display_format='MMM Do, YY ',
        min_date_allowed=dtmin,
        max_date_allowed=dt.now().date(),
        initial_visible_month=dt.now().date(),
        start_date = dtmin.date(),
        end_date = dtmax.date(),
    ),
    html.Div(id='output-container-date-picker-range')
    
])

app.css.append_css({
    "external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"
})

# @app.callback(Output('livegraph', 'figure'),[Input('interval-component', 'n_intervals'),Input('date-picker-range', 'start_date')],[State('livegraph', 'figure')])
# def update_graph_live(n, figure, start_date):
#     conn = psycopg2.connect(host="john.db.elephantsql.com",database="hibzxjxl", user="hibzxjxl", password="BbJmB-QJQegz1z8f4jmsfsUY0GsNXehi")

#     cur = conn.cursor()
#     cur.execute("SELECT * from timetrend")
#     # print("The number of parts: ", cur.rowcount)
#     row = cur.fetchone()
#     time=[]
#     cov=[]
#     while row is not None:
#                 # print(row)
#                 time.append(row[0])
#                 cov.append(row[1])
#                 row = cur.fetchone()
#     # print(n)
    
#     cur.close()
    
#     dtmin = min(time)
#     dtmax = max(time)

#     fig = go.Figure(
#         data = [go.Scatter(
#         x = time,
#         y = cov,
#         mode='lines',
#         )],
        
#     )
#     return fig



@app.callback(
    dash.dependencies.Output('livegraph', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def graph_update_on_range(start_date,end_date):
    end_date = dt.strptime(end_date, "%Y-%m-%d").date()
    start_date = dt.strptime(start_date, "%Y-%m-%d").date()
    conn = psycopg2.connect(host="john.db.elephantsql.com",database="hibzxjxl", user="hibzxjxl", password="BbJmB-QJQegz1z8f4jmsfsUY0GsNXehi")

    cur = conn.cursor()
    cur.execute("SELECT * from timetrend")
    # print("The number of parts: ", cur.rowcount)
    row = cur.fetchone()
    time=[]
    cov=[]
    while row is not None:
                # print(row)
                date = row[0].date()
                
                if date<end_date and date>start_date:
                    time.append(row[0])
                    cov.append(row[1])
                row = cur.fetchone()
    
    cur.close()
    fig = go.Figure(
        data = [go.Scatter(
        x = time,
        y = cov,
        mode='lines',
        )],
    
    )
    return fig


# @app.callback(
#     dash.dependencies.Output('output-container-date-picker-range', 'children'),
#     [dash.dependencies.Input('date-picker-range', 'start_date'),
#      dash.dependencies.Input('date-picker-range', 'end_date')])
# def update_output(start_date, end_date):
#     string_prefix = 'You have selected: '
#     if start_date is not None:
#         start_date = dt.strptime(start_date, '%Y-%m-%d')
#         start_date_string = start_date.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
#     if end_date is not None:
#         end_date = dt.strptime(end_date, '%Y-%m-%d')
#         end_date_string = end_date.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'End Date: ' + end_date_string
#     if len(string_prefix) == len('You have selected: '):
#         return 'Select a date to see it displayed here'
#     else:
#         return string_prefix

# @app.callback(Output('date-picker-range', 'start_date'),[Input('interval-component', 'n_intervals')],)
# def update_start_date(n):
#     conn = psycopg2.connect(host="john.db.elephantsql.com",database="hibzxjxl", user="hibzxjxl", password="BbJmB-QJQegz1z8f4jmsfsUY0GsNXehi")

#     cur = conn.cursor()
#     cur.execute("SELECT * from timetrend")
#     # print("The number of parts: ", cur.rowcount)
#     row = cur.fetchone()
#     time=[]
#     cov=[]
#     while row is not None:
#                 # print(row)
#                 time.append(row[0])
#                 cov.append(row[1])
#                 row = cur.fetchone()
#     # print(n)
    
#     cur.close()
#     start_date = min(time)
#     return start_date

# @app.callback(Output('date-picker-range', 'end_date'),[Input('date-picker-range', 'start_date')],)
# def update_end_date(n):
#     conn = psycopg2.connect(host="john.db.elephantsql.com",database="hibzxjxl", user="hibzxjxl", password="BbJmB-QJQegz1z8f4jmsfsUY0GsNXehi")

#     cur = conn.cursor()
#     cur.execute("SELECT * from timetrend")
#     # print("The number of parts: ", cur.rowcount)
#     row = cur.fetchone()
#     time=[]
#     cov=[]
#     while row is not None:
#                 # print(row)
#                 time.append(row[0])
#                 cov.append(row[1])
#                 row = cur.fetchone()
#     # print(n)
    
#     cur.close()
#     end_date = max(time)
#     print(end_date)
#     return end_date
    



if __name__ == '__main__':
    app.run_server(debug=True)
