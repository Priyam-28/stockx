# dashboard/app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import threading
import time
from market.core import GlobalMarket

# Initialize market
market = GlobalMarket()

# Start market updates in a separate thread
def run_market():
    while True:
        market.update_prices()
        time.sleep(60)  # Update every 60 seconds

market_thread = threading.Thread(target=run_market, daemon=True)
market_thread.start()

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Virtual Stock Market Dashboard"),
    
    # Price Charts
    html.H2("Live Price Charts"),
    dcc.Graph(id='price-chart'),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0),  # Update every 60 seconds
    
    # Order Book
    html.H2("Order Book"),
    html.Div(id='order-book'),
    
    # Sentiment Analysis
    html.H2("Meme Coin Sentiment"),
    dcc.Graph(id='sentiment-chart')
])

# Callback to update price charts
@app.callback(
    Output('price-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_price_chart(n):
    data = []
    for symbol, asset in market.assets.items():
        data.append(go.Scatter(
            x=pd.date_range(end=pd.Timestamp.now(), periods=10, freq='min'),  # Last 10 minutes
            y=[asset.price] * 10,  # Simulated price history
            mode='lines',
            name=symbol
        ))
    return {'data': data, 'layout': go.Layout(title="Live Asset Prices")}

# Callback to update order book
@app.callback(
    Output('order-book', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_order_book(n):
    order_book = []
    for symbol in market.assets:
        buy_orders = sum(market.player_activity['buy'].get(symbol, []))
        sell_orders = sum(market.player_activity['sell'].get(symbol, []))
        order_book.append(html.Div([
            html.H3(symbol),
            html.P(f"Buy Orders: {buy_orders}"),
            html.P(f"Sell Orders: {sell_orders}")
        ]))
    return order_book

# Callback to update sentiment analysis
@app.callback(
    Output('sentiment-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_sentiment_chart(n):
    data = []
    for symbol, asset in market.assets.items():
        if asset.asset_type == 'meme':
            data.append(go.Bar(
                x=[symbol],
                y=[asset.sentiment],
                name=symbol
            ))
    return {'data': data, 'layout': go.Layout(title="Meme Coin Sentiment")}

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)