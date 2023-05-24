import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import streamlit as st
from matplotlib import pyplot as plt, dates as mdates
from pathlib import Path
# from google.oauth2 import service_account
# from google.cloud import storage

def read_file(stock):
    data = yf.Ticker(stock)
    data = data.history('3mo')
    data.reset_index(inplace=True)
    return data

# def read_file(stock):
#     bucket_name = 'streamlit-stocks-data'
#     credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
#     client = storage.Client(credentials=credentials)
#     bucket = client.bucket(bucket_name)
#     blob = bucket.get_blob(f'{stock}.csv')
#     df = []
#     content = ''
#     if storage.Blob(bucket=bucket, name=f'{stock}.csv').exists(client) and str(blob.updated)[:10] == str(dt.date.today()): 
#         #checks if the file stock exists and if its last updated and if it isn't we will upload a new version
#         content = bucket.blob(f'{stock}.csv').download_as_string().decode("utf-8")
#     else: 
#         data = yf.Ticker(stock)
#         data = data.history('3mo')
#         data.reset_index(inplace=True)
#         upload_blob(pd.DataFrame.to_string(data), f'{stock}.csv')
#         content = bucket.blob(f'{stock}.csv').download_as_string().decode("utf-8")
#     if len(content) == 84:
#          raise Exception()
#     else:
#         content = content.strip().split('\n') #if content array is 1, raise invalid stock error
#         for row in content[1:]:
#             row = row.split(' ')
#             row = row[1:]
#             while '' in row:
#                 row.remove('')
#             date = row[0]
#             row = [float(e) for e in row[1:]]
#             row.insert(0, date)
#             df.append(row)
#         df = pd.DataFrame(df, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
#         return df

# def upload_blob(contents, destination_name):
#     credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
#     client = storage.Client(credentials=credentials)
#     bucket = client.get_bucket('streamlit-stocks-data')
#     blob = bucket.blob(destination_name)
#     blob.upload_from_string(contents)
    
def multi_plot(symbol, emas, stock_color): #emas is a dictionary {ma_length:color}
    plt.style.use('dark_background')
    fig, ax = plt.subplots(nrows=len(symbol), ncols=1)
    ax[0].set_title('Stock Prices')
    for i in range(len(symbol)):
        data = read_file(symbol[i])
        data['Date'] = pd.to_datetime(data['Date'])
        ax[i].set_xlim(data.iloc[0,0], data.iloc[data.shape[0]-1, 0])
        ax[i].plot(data['Date'], data['Close'], label='Close Price', color=stock_color)
        ax[i].tick_params(labelbottom=False, labelsize=6)
        for ema in emas:  
            ax[i].plot(data.iloc[ema-1:, 0], calculate_ma(ema, data), label=f'{ema} Day EMA', color=emas[ema])        
        ax[i].set_ylabel(symbol[i])
        if i == len(symbol)-1:
                ax[i].set_xlabel('Dates')
                ax[i].tick_params(labelbottom=True, labelsize=6)
                ax[i].legend(bbox_to_anchor=(0, -0.05), fontsize=6)
    plt.subplots_adjust(left=0.05, right=.75, hspace=0)
    plt.xticks(rotation=30)
    return fig

def single_plot(symbol, emas, stock_color):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(nrows=len(symbol), ncols=1)
    ax.set_title('Stock Prices')
    data = read_file(symbol[0])
    data['Date'] = pd.to_datetime(data['Date'])
    ax.set_xlim(data.iloc[0,0], data.iloc[data.shape[0]-1, 0])
    ax.plot(data['Date'], data['Close'], label='Close Price', color=stock_color)
    ax.tick_params(labelbottom=False, labelsize=6)
    for ema in emas:  
        ax.plot(data.iloc[ema-1:, 0], calculate_ma(ema, data), label=f'{ema} Day EMA', color=emas[ema])

    ax.set_ylabel(symbol[0])
    ax.set_xlabel('Dates')
    ax.tick_params(labelbottom=True, labelsize=6)
    ax.legend(bbox_to_anchor=(0, 0), fontsize=6)
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
        ema.append(((data.iloc[i, 4] - ema[i-ema_length-1]) * multiplier) + ema[i-ema_length-1])
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

stock = read_file('AMD')
#print(len(calculate_rsi(14, stock)))
#print(dt.date.today())