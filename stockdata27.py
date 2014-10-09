import yahoofinance27
import numpy

def stockdata(symbol, start_date, end_date):
    """
    Get historical prices for an array of ticker symbols.
    Symbol format is 'symbol'
    Date format is 'YYYYMMDD'
    By VC Analytics on 10/06/2014
    """

    date = [ ]
    open = [ ]
    high = [ ]
    low = [ ]
    close = [ ]
    vol = [ ]
    adjclose = [ ]

    for i in range(len(symbol)):
        if i == 0:
            datetemp, opentemp, hightemp, lowtemp, closetemp, voltemp, adjclosetemp = yahoofinance27.get_historical_prices(symbol[i], start_date, end_date)
            opentemp = numpy.array(opentemp,dtype='|S4').astype(numpy.float)
            hightemp = numpy.array(hightemp,dtype='|S4').astype(numpy.float)
            lowtemp = numpy.array(lowtemp,dtype='|S4').astype(numpy.float)
            closetemp = numpy.array(closetemp,dtype='|S4').astype(numpy.float)
            voltemp = numpy.array(voltemp,dtype='|S4').astype(numpy.float)
            adjclosetemp = numpy.array(adjclosetemp,dtype='|S4').astype(numpy.float)
            opentemp = (opentemp * adjclosetemp / closetemp)
            hightemp = (hightemp * adjclosetemp / closetemp)
            lowtemp = (lowtemp * adjclosetemp / closetemp)
            closetemp = (closetemp * adjclosetemp / closetemp)
            date.append(datetemp.tolist())
            open.append(opentemp.tolist())
            high.append(hightemp.tolist())
            low.append(lowtemp.tolist())
            close.append(closetemp.tolist())
            vol.append(voltemp.tolist())
            adjclose.append(adjclosetemp.tolist())
			
        else:
            datetemp, opentemp, hightemp, lowtemp, closetemp, voltemp, adjclosetemp = yahoofinance27.get_historical_prices(symbol[i], start_date, end_date)
            opentemp = numpy.array(opentemp,dtype='|S4').astype(numpy.float)
            hightemp = numpy.array(hightemp,dtype='|S4').astype(numpy.float)
            lowtemp = numpy.array(lowtemp,dtype='|S4').astype(numpy.float)
            closetemp = numpy.array(closetemp,dtype='|S4').astype(numpy.float)
            voltemp = numpy.array(voltemp,dtype='|S4').astype(numpy.float)
            adjclosetemp = numpy.array(adjclosetemp,dtype='|S4').astype(numpy.float)
            opentemp = (opentemp * adjclosetemp / closetemp)
            hightemp = (hightemp * adjclosetemp / closetemp)
            lowtemp = (lowtemp * adjclosetemp / closetemp)
            closetemp = (closetemp * adjclosetemp / closetemp)
            adjclosetemp = adjclosetemp
            date.append(datetemp.tolist())
            open.append(opentemp.tolist())
            high.append(hightemp.tolist())
            low.append(lowtemp.tolist())
            close.append(closetemp.tolist())
            vol.append(voltemp.tolist())
            adjclose.append(adjclosetemp.tolist())

    return date, open, high, low, close, vol, adjclose