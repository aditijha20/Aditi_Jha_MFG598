#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 19:15:04 2024

@author: aditijha20
"""

from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd

# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Stock Price and Recommendations"),
    html.Label("Enter Stock Symbol:"),
    dcc.Input(id="stock-symbol-input", type="text", placeholder="Enter stock symbol", value="TSLA"),
    html.Label("Enter Number of Years for Historical Data:"),
    dcc.Input(id="years-input", type="number", placeholder="Enter number of years", value=1),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0),  # Interval component to trigger updates
    html.Div([
        dcc.Graph(id='stock-chart'),
    ]),
    html.Div([
        dcc.Graph(id='volume-chart'),
    ]),
    html.Div(id='recommendations-output'),
])

# Callback to update the stock chart, volume chart, and recommendations output
@app.callback(
    [Output('stock-chart', 'figure'),
     Output('volume-chart', 'figure'),
     Output('recommendations-output', 'children')],
    Input('interval-component', 'n_intervals'),
    Input('stock-symbol-input', 'value'),
    Input('years-input', 'value')
)
def update_charts_and_recommendations(n, stock_symbol, years):
    # Convert years to integer
    years = int(years)
    
    # Create a Ticker object
    ticker = yf.Ticker(stock_symbol)
    
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(years=years)
    
    # Get historical market data with custom date range
    data = ticker.history(start=start_date, end=end_date)
    
    # Create the stock price plot
    stock_fig = go.Figure()
    stock_fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    stock_fig.add_trace(go.Scatter(x=data.index, y=data['Open'], mode='lines', name='Open'))
    stock_fig.update_layout(title=f"{stock_symbol} Stock Price", xaxis_title='Date', yaxis_title='Price')
    
    # Create the volume plot
    volume_fig = go.Figure()
    volume_fig.add_trace(go.Scatter(x=data.index, y=data['Volume'], mode='lines', name='Volume'))
    volume_fig.update_layout(title=f"{stock_symbol} Stock Volume", xaxis_title='Date', yaxis_title='Volume')

    # Get recommendations
    recommendations = ticker.recommendations
    recommendations_text = recommendations.to_string(index=False)

    return stock_fig, volume_fig, html.Pre(recommendations_text)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
