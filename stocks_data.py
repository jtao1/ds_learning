import pandas as pd
import numpy as np
import yfinance as yf
from matplotlib import pyplot as plt, dates as mdates


def read_file(stock):
    data = yf.Ticker(stock)
    data = data.history('6mo')
    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

def plot(symbol, emas, stock_color): #emas is a dictionary {ma_length:color}
    plt.style.use('dark_background')
    fig, ax = plt.subplots(nrows=len(symbol), ncols=1)
    ax = [ax] if len(symbol) == 1 else ax
    ax[0].set_title('Stock Prices')
    for i in range(len(symbol)):
        data = read_file(symbol[i])
        ax[i].set_xlim(data.iloc[0,0], data.iloc[data.shape[0]-1, 0])
        ax[i].plot(data['Date'], data['Close'], label='Close Price', color=stock_color)
        ax[i].xaxis.set_major_formatter(mdates.DateFormatter('%b'))        
        ax[i].grid(True, color='#414242')
        ax[i].tick_params(labelbottom=False, labelsize=6)
        for ema in emas:  
            ax[i].plot(data.iloc[ema-1:, 0], calculate_ma(ema, data), label=f'{ema} Day EMA', color=emas[ema])        
        ax[i].set_ylabel(symbol[i])
    last = len(symbol)-1
    ax[last].set_xlabel('Dates')
    ax[last].tick_params(labelbottom=True, labelsize=6)
    ax[last].legend(bbox_to_anchor=(0, -0.05), fontsize=6)
    plt.subplots_adjust(left=0.05, right=.75, hspace=0)
    plt.xticks(rotation=30)
    return fig

def calculate_ma(ema_length, data):
    #to calculate ema: ignore first ma_length days, for ma_length+1 day take average of the previous ma_length days
    #for the day our equation: (((close - prev ema) * multiplier) + prev ema)
    #multiplier: (2 / ma_length + 1)
    ema = []
    multiplier = 2 / (ema_length+1) 
    ema.append(np.average(data.iloc[0:ema_length, 4]))
    for i in range(ema_length, data.shape[0]):
        ema.append(((data.iloc[i, 4] - ema[i-ema_length]) * multiplier) + ema[i-ema_length])
    return ema

def calculate_rsi(rsi_length, data):
    #rsi = 100 - (100/(1+rs)) where rs = average gain / average loss
    #default time period of 14
    #ignore first day
    rsi = []
    change = {'gains':[], 'losses':[]}  
    for i in range(len(data)-1):
        price_change = data.iloc[i+1, 4] - data.iloc[i, 4]
        if price_change > 0:
            change['gains'].append(price_change)
            change['losses'].append(0)
        elif price_change < 0:
            change['gains'].append(0)
            change['losses'].append(abs(price_change))
        else:
            change['gains'].append(0)
            change['losses'].append(0)
        if len(change['gains']) == rsi_length:
            rs = np.mean(change['gains']) / np.mean(change['losses'])
            rsi.append(100-(100/(1+rs)))
            change['gains'].pop(0)
            change['losses'].pop(0)
    return rsi