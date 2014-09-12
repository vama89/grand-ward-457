
import yahoofinance as yf
import numpy as np

def stockdata(symbol, start_date, end_date):
    
    for i in range(len(symbol)):
        if i == 0:
            date, open, high, low, close, vol, adjclose = yf.get_historical_prices(symbol[i], start_date, end_date)
            open = np.array(open,dtype='|S4').astype(np.float)
            high = np.array(high,dtype='|S4').astype(np.float)
            low = np.array(low,dtype='|S4').astype(np.float)
            close = np.array(close,dtype='|S4').astype(np.float)
            vol = np.array(vol,dtype='|S4').astype(np.float)
            adjclose = np.array(adjclose,dtype='|S4').astype(np.float)
        else:
            datetemp, opentemp, hightemp, lowtemp, closetemp, voltemp, adjclosetemp = yf.get_historical_prices(symbol[i], start_date, end_date)
            opentemp = np.array(opentemp,dtype='|S4').astype(np.float)
            hightemp = np.array(hightemp,dtype='|S4').astype(np.float)
            lowtemp = np.array(lowtemp,dtype='|S4').astype(np.float)
            closetemp = np.array(closetemp,dtype='|S4').astype(np.float)
            voltemp = np.array(voltemp,dtype='|S4').astype(np.float)
            adjclosetemp = np.array(adjclosetemp,dtype='|S4').astype(np.float)
            open = np.vstack([open,opentemp])
            high = np.vstack([high,hightemp])
            low = np.vstack([low,lowtemp])
            close = np.vstack([close,closetemp])
            vol = np.vstack([vol,voltemp])
            adjclose = np.vstack([adjclose,adjclosetemp])

    return date, open, high, low, close, vol, adjclose

"""
symbol has to be in matrix form
date = np.asmatrix(date)
open = np.asmatrix(open)
high = np.asmatrix(high)
low = np.asmatrix(low)
close = np.asmatrix(close)
vol = np.asmatrix(vol)
adjclose = np.asmatrix(adjclose)
import stockdata as sd
symbol = ['aapl','goog']
a,b,c,d,e,f,g=sd.stockdata(symbol, start_date, end_date)
"""