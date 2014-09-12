
import yahoofinance27
import numpy

def stockdata(symbol, start_date, end_date):
    
    for i in range(len(symbol)):
        if i == 0:
            date, open, high, low, close, vol, adjclose = yahoofinance27.get_historical_prices(symbol[i], start_date, end_date)
            open = numpy.array(open,dtype='|S4').astype(numpy.float)
            high = numpy.array(high,dtype='|S4').astype(numpy.float)
            low = numpy.array(low,dtype='|S4').astype(numpy.float)
            close = numpy.array(close,dtype='|S4').astype(numpy.float)
            vol = numpy.array(vol,dtype='|S4').astype(numpy.float)
            adjclose = numpy.array(adjclose,dtype='|S4').astype(numpy.float)
        else:
            datetemp, opentemp, hightemp, lowtemp, closetemp, voltemp, adjclosetemp = yahoofinance27.get_historical_prices(symbol[i], start_date, end_date)
            opentemp = numpy.array(opentemp,dtype='|S4').astype(numpy.float)
            hightemp = numpy.array(hightemp,dtype='|S4').astype(numpy.float)
            lowtemp = numpy.array(lowtemp,dtype='|S4').astype(numpy.float)
            closetemp = numpy.array(closetemp,dtype='|S4').astype(numpy.float)
            voltemp = numpy.array(voltemp,dtype='|S4').astype(numpy.float)
            adjclosetemp = numpy.array(adjclosetemp,dtype='|S4').astype(numpy.float)
            open = numpy.vstack([open,opentemp])
            high = numpy.vstack([high,hightemp])
            low = numpy.vstack([low,lowtemp])
            close = numpy.vstack([close,closetemp])
            vol = numpy.vstack([vol,voltemp])
            adjclose = numpy.vstack([adjclose,adjclosetemp])

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