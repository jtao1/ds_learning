import requests
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt, dates as mdates
import datetime as dt
import yfinance as yf
from pathlib import Path

def get_data(stock, fname):
    data = yf.Ticker(stock)
    pd.DataFrame.to_csv(data.history(period='3mo'), path_or_buf=fname)

def check_data(stocks):
    for stock in stocks:
        fname = f'./Stock-Data/{stock}.csv'
        path = Path(fname)
        if path.is_file():
            data = pd.read_csv(fname)
            if data.iloc[data.shape[0]-1, 0] != dt.date.today: #will upade csv if it doesn't have today's closing price
                get_data(stock, fname)
        else:
            get_data(stock, fname)

def multi_plot(symbol, mas, stock_color): #mas is a dictionary {ma_length:color}
    plt.style.use('dark_background')
    fig, ax = plt.subplots(len(symbol), 1)        
    ax[0].set_title('Stock Prices')
    for i in range(len(symbol)):
        data = pd.read_csv(f'./Stock-Data/{symbol[i]}.csv')
        #data = data.iloc[::-1].reset_index(drop=True)
        data['Date'] = pd.to_datetime(data['Date'])
        ax[i].set_xlim(data.iloc[0,0], data.iloc[data.shape[0]-1, 0])
        ax[i].plot(data['Date'], data['Close'], label='Close Price', color=stock_color)
        ax[i].tick_params(labelbottom=False, labelsize=6)
        for ma in mas:  
            ax[i].plot(data.iloc[ma-1:, 0], calculate_ma(ma, data), label=f'{ma} Day EMA', color=mas[ma])        
        ax[i].set_ylabel(symbol[i])
        if i == len(symbol)-1:
                ax[i].set_xlabel('Dates')
                ax[i].tick_params(labelbottom=True, labelsize=6)
                ax[i].legend(bbox_to_anchor = (1.2, 3.15), fontsize=6)

    plt.subplots_adjust(left=0.05, right=.75, hspace=0)
    plt.xticks(rotation=30)
    return fig

def calculate_ma(ma_length, data):
    #to calculate ema: ignore first ma_length days, for ma_length+1 day take average of the previous ma_length days
    #for the day our equation: (((close - prev ema) * multiplier) + prev ema)
    #multiplier: (2 / ma_length + 1)
    ma = []
    multiplier = 2 / (ma_length+1) 
    ma.append(np.average(data.iloc[0:ma_length, 4]))
    for i in range(ma_length, data.shape[0]):
        ma.append(((data.iloc[i, 4] - ma[i-ma_length-1]) * multiplier) + ma[i-ma_length-1])
    return ma