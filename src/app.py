
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

################### FOR AUTHORIZATION ##############
import dash_auth

USERNAME_PASSWORD_PAIRS = [['username','password'],
                           ['JamesBond','gango']]

###################################################

import pandas as pd
import pandas_datareader as pdr

from datetime import date
import os
import yfinance as yf

# df = pdr.get_markets_iex()


app = dash.Dash()

################### FOR AUTHORIZATION ##############
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
####################################################

################### FOR AUTHORIZATION ##############
server = app.server
####################################################

nsdq = pd.read_csv('NASDAQcompanylist.csv')
print(nsdq.head())

options = []

for ticker in nsdq['Symbol']:
    #{'label':'user sees', 'value':'script sees'}
    options_dict = {}
    options_dict['label'] = nsdq[nsdq['Symbol'] == ticker]['Name'].values[0] +' '+ticker
    options_dict['value'] = ticker
    options.append(options_dict)

# print(options_dict)
# print(options)


app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Stock Company'),
            dcc.Dropdown(id='dropdown-filter',
                        options = options,
                        value = ['TSLA'], 
                        multi = True)
        ]),
        html.Div([
            html.H1('Stock Dates Start'),
            dcc.DatePickerRange( id='date-filter',
                start_date=date(2022, 1, 1),
                end_date = date(2023,1,1),
                min_date_allowed=date(2015,1,1),
                max_date_allowed=date.today()
            )
        ]),
        # html.Div([
        #     html.H1('Stock Input'),
        #     dcc.Input(id='input-filter', value = 'TSLA')
        # ]),
        html.Button(id='submit-button', children='Submit Here', n_clicks=0)
    ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content':'space-evenly'}),


    html.Div([
        html.H1('Graph Header'),
        dcc.Graph(id='graph',
                  figure= {
                      'data': [go.Scatter(
                          x=[0,1],
                          y=[0,1],
                          mode = 'lines'
                      )],
                      'layout': go.Layout(title='Graph Title')
                  })
    ])
])


@app.callback(Output('graph','figure'),
              [Input('submit-button', 'n_clicks')],
              [State('dropdown-filter', 'value'),
               State('date-filter', 'start_date'),
               State('date-filter', 'end_date')])
def update_title(n_clicks,stock_ticker,start_date,end_date):
    # df = pdr.get_data_tiingo('AAPL', api_key=os.getenv('TIINGO_API_KEY'))
    traces = []


    print('-----------')
    print(stock_ticker)
    for tic in stock_ticker:
        print(tic)
        ticker = yf.Ticker(tic)
        df = ticker.history(start=start_date, end=end_date)
        traces.append({'x': df.index, 'y':df['Close'], 'name': tic})
    print(df.head())
    print(df.columns)

    layout = go.Layout(title = 'Stocks')

    fig = {
        'data': traces,
        'layout': layout
    }

    # fig = {
    #     'data': [go.Scatter(x=df_new.index,
    #                         y=df_new['Close'],
    #                         name = 'cringe')for df_new in traces],
    #     'layout': layout
    # }

    # print('-------------------------------')
    # print(stock_ticker)
    # print('-------------------------------')
    # print(traces)
    return fig

# print('-------------------------------')
# print(options[0]['value'])


if __name__ == '__main__':
    app.run_server()