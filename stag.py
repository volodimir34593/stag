import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

class TechnicalIndicator:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date

    def get_price_data(self):
        data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        return data

    def calculate_indicator(self, data, indicator='SMA', window=20):
        if indicator == 'SMA':
            data['SMA'] = data['Close'].rolling(window=window).mean()
        # Додайте інші індикатори за необхідності

        return data

    def plot_data(self, data):
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'],
                                     name='Цінові свічки'))
        if 'SMA' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA'], mode='lines', name='SMA'))

        fig.update_layout(title='Графік ціни та технічного індикатора',
                          xaxis_title='Дата',
                          yaxis_title='Ціна')
        fig.show()

# Задаємо параметри та виконуємо код
symbol = 'AAPL'
start_date = '2023-01-01'
end_date = '2023-12-31'

indicator = TechnicalIndicator(symbol, start_date, end_date)
price_data = indicator.get_price_data()
indicator_data = indicator.calculate_indicator(price_data)
indicator.plot_data(indicator_data)
