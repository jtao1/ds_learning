import pandas as pd
import yfinance as yf
import indicators
from matplotlib import pyplot as plt, dates as mdates

def read_file(stock):
    data = yf.Ticker(stock)
    data = data.history('6mo')
    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

def plot(symbol, ema_data, rsi, stock_color): #emas is a dictionary {ma_length:color}

    emas, ema_stock = ema_data
    nrows = len(symbol) + len(rsi)

    plt.style.use('dark_background')

    fig, ax = plt.subplots(nrows=nrows, ncols=1, sharex=True)
    ax = [ax] if len(symbol) == 1 else ax
    ax[0].set_title('Stock Prices')
    rown = 0
    for stock in symbol:
        data = read_file(stock)
        ax[rown].set_xlim(data.iloc[0,0], data.iloc[data.shape[0]-1, 0])
        ax[rown].plot(data['Date'], data['Close'], label='Close Price', color=stock_color)
        ax[rown].grid(True, color='#414242')
        ax[rown].tick_params(labelbottom=False, labelsize=6)
        ax[rown].set_ylabel(stock)
        for spine in ax[rown].spines.values():
            spine.set_color('#8c8d91')
            spine.set_linewidth(2)
        ax[rown].spines['bottom'].set_linewidth(1)

        if stock in ema_stock:
            for ema in emas:  
                ax[rown].plot(data.iloc[ema-1:, 0], indicators.calculate_ma(ema, data), label=f'{ema} Day EMA', color=emas[ema])
        if stock in rsi:
            rown += 1
            ax[rown].plot(data.iloc[14:, 0], indicators.calculate_rsi(data), label = 'RSI', color='#9949FF')
            ax[rown].axhline(30, linestyle='dotted', linewidth=1.5, color='#EFF988', alpha=0.7)
            ax[rown].axhline(70, linestyle='dotted', linewidth=1.5, color='#73CBFA', alpha=0.7)
            ax[rown].set_ylim(0, 100)
            ax[rown].set_yticks([30, 50, 70])
            ax[rown].tick_params(axis='y', labelsize=4)
            for spine in ax[rown].spines.values():
                spine.set_color('#8c8d91')
                spine.set_linewidth(2)
            ax[rown].spines['top'].set_linewidth(0.1)

        else:
            ax[rown].spines['bottom'].set_linewidth(2)
        rown += 1
    ax[rown - 1].set_xlabel('Dates')
    ax[rown - 1].tick_params(axis='x', labelbottom=True, labelsize=6)
    ax[rown - 1].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    

    plt.subplots_adjust(left=0.05, right=.75, hspace=0)
    plt.xticks(rotation=30)
    return fig