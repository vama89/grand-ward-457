from urllib.request import Request, urlopen
from urllib.parse import urlencode
import numpy as np

def get_historical_prices(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'

    Returns a nested dictionary (dict of dicts).
    outer dict keys are dates ('YYYYMMDD')
    """	

    params = urlencode({
        's': symbol,
        'a': int(start_date[4:6]) - 1,
        'b': int(start_date[6:8]),
        'c': int(start_date[0:4]),
        'd': int(end_date[4:6]) - 1,
        'e': int(end_date[6:8]),
        'f': int(end_date[0:4]),
        'g': 'd',
        'ignore': '.csv',
    })
    url = 'http://ichart.yahoo.com/table.csv?%s' % params
    req = Request(url)
    resp = urlopen(req)
    content = str(resp.read().decode('utf-8').strip())
    daily_data = content.splitlines()
    t = len(daily_data)
    data = daily_data[1].split(',')
    for i in range(2,t):
        datatemp = daily_data[i].split(',')
        data = np.c_[data,datatemp]
    datetemp = data[0]
    opentemp = data[1]
    hightemp = data[2]
    lowtemp = data[3]
    closetemp = data[4]
    voltemp = data[5]
    adjclosetemp = data[6]
    datetemp = datetemp[::-1]
    opentemp = opentemp[::-1]
    hightemp = hightemp[::-1]
    lowtemp = lowtemp[::-1]
    closetemp = closetemp[::-1]
    voltemp = voltemp[::-1]
    adjclosetemp = adjclosetemp[::-1]
    date = datetemp
    open = opentemp
    high = hightemp
    low = lowtemp
    close = closetemp
    vol = voltemp
    adjclose = adjclosetemp

    return date, open, high, low, close, vol, adjclose

"""
	t = sum(1 for row in daily_data)
	data = daily_data[1].split(',')
	for i in range(2,t):
		datatemp = daily_data[i].split(',')
		data = np.c_[data,datatemp]
"""
	
"""
data = [day[:-2].split(',') for day in days]
import yahoofinance as yf
data = yf.get_historical_prices(...)
python yahoofinance.py aapl m 20031201 20140801
"""