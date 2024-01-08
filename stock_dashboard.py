# Libraries
import pandas as pd
import yfinance as yf
import datetime as dt
import plotly.graph_objects as go
import requests
import bs4
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input

# -------------------------------------------------------------------------------------------
# Getting and preparing data using API
tickers = ['PETR4.SA', 'WEGE3.SA', 'CEAB3.SA']

n_years = 1
end_date = dt.datetime.now()
start_date = end_date - dt.timedelta(days=365*n_years)
df = yf.download(tickers=tickers, start=start_date, end=end_date)
tickers = [ticker.replace('.SA','') for ticker in tickers]
df = df.drop(columns=['Adj Close', 'Volume']).reset_index()
df = df.rename(columns={'PETR4.SA': tickers[0],
                        'WEGE3.SA': tickers[1],
                        'CEAB3.SA': tickers[2]})

## -------------------------------------------------------------------------------------------
## Web scrapping
#ticker_dict = {tickers[0]:'petrobras',
#              tickers[1]:'weg',
#              tickers[2]:'c%26a'}
#
#ticker = tickers[0]
#ticker_name = ticker_dict[ticker]
#request = requests.get('https://braziljournal.com/?s='+ticker_name)
#page_soup = bs4.BeautifulSoup(request.text, 'html.parser')
#page_info = page_soup.find_all('figcaption', class_='boxarticle-infos', limit=3)
#titles = []
#links = []
#
#for n in range(len(page_info)):
#    page_len = len(page_info[n].find_all('a'))
#    aux1 = [page_info[n].find_all('a')[i].text.strip() for i in range(page_len)]
#    aux2 = [page_info[n].find_all('a')[i].attrs['href'].strip() for i in range(page_len)]
#    titles.append(aux1)
#    links.append(aux2)

# -------------------------------------------------------------------------------------------
# App layout
#app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app = Dash(__name__)
server = app.server

app.layout = dbc.Container([

    dbc.Row([

        dbc.Col([

            dbc.Row([
                dcc.Dropdown(id = 'dropdown-selector',
                         options = tickers,
                         value = tickers[0],
                         style= dict(width='50%')
                         ),
            
            ], align='center'),
            
            dbc.Row([
                dcc.Graph(id = 'candle-graph', figure={}, className='bg-dark')
            ]),
        ], width={'size':6}),

        dbc.Col([

            dbc.Row([
                html.H1('Últimas notícias', className='text-center')
                ]),
            
            dbc.Row([
                html.Div(children='', id='last_news', className="text-white")
                #dcc.Markdown(children='', id='last_news')
            ])

        ], align='center', width={'size':6})

    ])

], fluid=True, style={'margin-top': 150})


@callback(
        Output(component_id = 'candle-graph', component_property = 'figure'),
        Input(component_id = 'dropdown-selector', component_property = 'value')
    )
def update_graph(value):
    print(value)   
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                     open=df['Open'][value],
                                     high=df['High'][value],
                                     low=df['Low'][value],
                                     close=df['Close'][value])])
    fig.update_layout(height = 550,
                  #width = 1000,
                  margin_b = 40,
                  margin_r = 40,
                  margin_t = 40,
                  margin_l = 40,
                  #paper_bgcolor = 'bg-dark',
                  #plot_bgcolor = 'black',
                  #font_color = 'white',
                  xaxis_rangeslider_visible=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig

@callback(
    Output(component_id='last_news', component_property='children'),
    Input(component_id='dropdown-selector', component_property='value')
)
def web_scrapping(ticker):
    print(ticker)
    ticker_dict = {tickers[0]:'petrobras',
              tickers[1]:'weg',
              tickers[2]:'c%26a'}

    #ticker = tickers[0]
    ticker_name = ticker_dict[ticker]
    request = requests.get('https://braziljournal.com/?s='+ticker_name)
    page_soup = bs4.BeautifulSoup(request.text, 'html.parser')
    page_info = page_soup.find_all('figcaption', class_='boxarticle-infos', limit=3)
    titles = []
    links = []

    for n in range(len(page_info)):
        page_len = len(page_info[n].find_all('a'))
        aux1 = [page_info[n].find_all('a')[i].text.strip() for i in range(page_len)]
        aux2 = [page_info[n].find_all('a')[i].attrs['href'].strip() for i in range(page_len)]
        titles.append(aux1)
        links.append(aux2)
        #print(titles)
        #print(links)
    result = [
        html.P(html.A(f'{titles[0][0]}', href=f'{links[0][0]}', className="text-decoration-none text-white")),
        html.H3(html.A(f'{titles[0][1]}', href=f'{links[0][1]}', className="text-decoration-none text-white")),
        html.Br(),
        html.P(html.A(f'{titles[1][0]}', href=f'{links[1][0]}', className="text-decoration-none text-white")),
        html.H3(html.A(f'{titles[1][1]}', href=f'{links[1][1]}', className="text-decoration-none text-white")),
        html.Br(),
        html.P(html.A(f'{titles[2][0]}', href=f'{links[2][0]}', className="text-decoration-none text-white")),
        html.H3(html.A(f'{titles[2][1]}', href=f'{links[2][1]}', className="text-decoration-none text-white"))
    ]
    #print(result)
    return result

if __name__ == '__main__':
    app.run_server(debug=False)


