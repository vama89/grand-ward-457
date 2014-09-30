import stockdata27
import returns27
import portfoliomv27
import numpy
import json

def results(symbol, start_date, end_date, what):
    """
    Computes the results of the minimum variance portfolio
    """

    a, b, c, d, e, f, g=stockdata27.stockdata(symbol, start_date, end_date)
    returns, Mu, Sigma=returns27.returns(g)

    if what == 'staticshort':
        Mu_mv,sigma_mv,Theta_mv=portfoliomv27.portfoliomv(Mu, Sigma)
    elif what == 'staticnoshort':
        Mu_mv, sigma_mv, Theta_mv = portfoliomv27.portfoliomvns(Mu, Sigma)

    return Mu_mv, sigma_mv, Theta_mv