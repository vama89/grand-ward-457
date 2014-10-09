import output27
import time

"""
By VC Analytics on 10/06/2014
"""

#symbol = ['wday','googl','fb','splk','aapl','ge','bac','lyg','ba']
#symbol = ['wday','googl','fb','splk','aapl']
symbol = ['wday','googl']
start_date = '20040101'
end_date = time.strftime("%Y%m%d")
# type = 'Minimum Variance Portfolio - Short'
type = 'Minimum Variance Portfolio - No Short'

Mu_mv, sigma_mv, Theta_mv, symbolsort = output27.results(symbol, start_date, end_date, type)