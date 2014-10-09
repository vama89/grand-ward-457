import stockdata27
import returns27
import portfoliomv27
import mle27
import numpy
import json

def results(symbol, start_date, end_date, type):
    """
    Computes the results of the minimum variance portfolio
    By VC Analytics on 10/06/2014
    """

    #date, open, high, low, close, vol, adjclose = stockdata27.stockdata(symbol, start_date, end_date)
    #returns, Mu, Sigma=returns27.returns(numpy.matrix(adjclose))
    date, open, high, low, close, vol, adjclose, adjclosesort, symbolsort, ret, Mu, Sigma = mle27.mle(symbol, start_date, end_date)

    if type == 'Minimum Variance Portfolio - Short':
        Mu_mv,sigma_mv,Theta_mv=portfoliomv27.portfoliomv(Mu, Sigma)
    elif type == 'Minimum Variance Portfolio - No Short':
        Mu_mv, sigma_mv, Theta_mv = portfoliomv27.portfoliomvns(Mu, Sigma)

    return Mu_mv, sigma_mv, Theta_mv, symbolsort