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

    def calculate_indicator(self, data, indicators=['SMA', 'EMA', 'RSI'], windows=[20, 20, 14]):
        for i in range(len(indicators)):
            indicator = indicators[i]
            window = windows[i]

            if indicator == 'SMA':
                data['SMA'] = data['Close'].rolling(window=window).mean()
            elif indicator == 'EMA':
                data['EMA'] = data['Close'].ewm(span=window, adjust=False).mean()
            elif indicator == 'RSI':
                delta = data['Close'].diff(1)
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                avg_gain = gain.rolling(window=window).mean()
                avg_loss = loss.rolling(window=window).mean()
                rs = avg_gain / avg_loss
                data['RSI'] = 100 - (100 / (1 + rs))
       

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
        if 'EMA' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA'], mode='lines', name='EMA'))
        if 'RSI' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))

        fig.update_layout(title='Графік ціни та технічного індикатора',
                          xaxis_title='Дата',
                          yaxis_title='Ціна',
                          plot_bgcolor='black',  
                          paper_bgcolor='black')  
        fig.show()

# Задаємо параметри та виконуємо код
symbol = 'AAPL'
start_date = '2020-01-01'  # You can adjust the start date
end_date = '2023-12-31'

indicator = TechnicalIndicator(symbol, start_date, end_date)
price_data = indicator.get_price_data()
indicator_data = indicator.calculate_indicator(price_data)
indicator.plot_data(indicator_data)

