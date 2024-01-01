import numpy as np

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

def calculate_rsi(data):
    #rsi = 100 - (100/(1+rs)) where rs = average gain / average loss
    #default time period of 14
    #ignore first day
    rsi = []
    avg_change = {'gains':[], 'losses':[]}
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

        if len(change['gains']) == 14:
            avg_change['gains'].append(np.mean(change['gains']))
            avg_change['losses'].append(np.mean(change['losses']))
            rsi.append(100-(100/(1+(avg_change['gains'][-1]/avg_change['losses'][-1]))))
        elif len(change['gains']) > 14:
            avg_change['gains'].append(((avg_change['gains'][-1] * 13) + change['gains'][-1]) / 14)
            avg_change['losses'].append(((avg_change['losses'][-1] * 13) + change['losses'][-1]) / 14)
            rsi.append(100-(100/(1+(avg_change['gains'][-1]/avg_change['losses'][-1]))))
    return rsi