import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import streamlit as st
from matplotlib import pyplot as plt, dates as mdates
from pathlib import Path
from google.oauth2 import service_account
from google.cloud import storage

def read_file(stock):
    bucket_name = 'streamlit-stocks-data'
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    df = []
    content = ''
    if storage.Blob(bucket=bucket, name=f'{stock}.csv').exists(client):
        content = bucket.blob(f'{stock}.csv').download_as_string().decode("utf-8")
    else: 
        data = yf.Ticker(stock)
        data = data.history('3mo')
        data.reset_index(inplace=True)
        #data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
        upload_blob(pd.DataFrame.to_string(data), f'{stock}.csv')
        content = bucket.blob(f'{stock}.csv').download_as_string().decode("utf-8")
    if len(content) == 84:
         raise Exception()
    else:
        content = content.strip().split('\n') #if content array is 1, raise invalid stock error
        for row in content[1:]:
            row = row.split(' ')
            row = row[1:]
            while '' in row:
                row.remove('')
            date = row[0]
            row = [float(e) for e in row[1:]]
            row.insert(0, date)
            df.append(row)
        df = pd.DataFrame(df, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
        return df

def upload_blob(contents, destination_name):
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket('streamlit-stocks-data')
    blob = bucket.blob(destination_name)
    blob.upload_from_string(contents)
    
def multi_plot(symbol, mas, stock_color): #mas is a dictionary {ma_length:color}
    plt.style.use('dark_background')
    fig, ax = plt.subplots(nrows=len(symbol), ncols=1)
    ax[0].set_title('Stock Prices')
    for i in range(len(symbol)):
        data = read_file(symbol[i])
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
                ax[i].legend(bbox_to_anchor=(0, -0.05), fontsize=6)

    plt.subplots_adjust(left=0.05, right=.75, hspace=0)
    plt.xticks(rotation=30)
    return fig

def single_plot(symbol, mas, stock_color):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(nrows=len(symbol), ncols=1)
    ax.set_title('Stock Prices')
    data = read_file(symbol[0])
    data['Date'] = pd.to_datetime(data['Date'])
    ax.set_xlim(data.iloc[0,0], data.iloc[data.shape[0]-1, 0])
    ax.plot(data['Date'], data['Close'], label='Close Price', color=stock_color)
    ax.tick_params(labelbottom=False, labelsize=6)
    for ma in mas:  
        ax.plot(data.iloc[ma-1:, 0], calculate_ma(ma, data), label=f'{ma} Day EMA', color=mas[ma])  
    ax.set_ylabel(symbol[0])
    ax.set_xlabel('Dates')
    ax.tick_params(labelbottom=True, labelsize=6)
    ax.legend(bbox_to_anchor=(0, 0), fontsize=6)
    
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