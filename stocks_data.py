import requests
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt, dates as mdates
import datetime as dt

time_duration = 'TIME_SERIES_DAILY'
#symbol = ('SPY', 'AMD', 'TCEHY')
output_size = 'compact'
api_key = 'O7MX9KYNRJQ0BHP5'
datatype = 'csv'

#url = f'https://www.alphavantage.co/query?function={time_duration}&symbol={symbol}&output={output_size}&interval=5min&apikey={api_key}&datatype={datatype}'

def get_data(symbol):
    for stock in symbol:
        url = f'https://www.alphavantage.co/query?function={time_duration}&symbol={stock}&output={output_size}&interval=5min&apikey={api_key}&datatype={datatype}'
        print(url)
        r = requests.get(url).text
        with open(f'./Stock-Data/Stock-{stock}.csv', 'w') as file:
            file.write(r)

def multi_plot(symbol, mas): #mas is a dictionary {ma_length:color}
    plt.style.use('dark_background')
    fig, ax = plt.subplots(len(symbol), 1)        
    ax[0].set_title('Stock Prices')
    for i in range(len(symbol)):
        data = pd.read_csv(f'./Stock-Data/Stock-{symbol[i]}.csv')
        data = data.iloc[::-1].reset_index(drop=True)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        ax[i].set_xlim(data.iloc[0,0], data.iloc[99,0])
        ax[i].plot(data['timestamp'], data['close'], label='Close Price', color='#8EA08F')
        ax[i].tick_params(labelbottom=False, labelsize=6)
        for ma in mas:
            ax[i].plot(data.iloc[ma-1:, 0], calculate_ma(ma, data), label=f'{ma} Day MA', color=mas[ma])        
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
    for i in range(ma_length, 100):
        ma.append(((data.iloc[i, 4] - ma[i-ma_length-1]) * multiplier) + ma[i-ma_length-1])
    return ma


#get_data()