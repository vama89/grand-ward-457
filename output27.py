import stockdata27
import returns27
import portfoliomv27
import numpy
import rpy2.robjects
from rpy2.robjects.numpy2ri import numpy2ri
import json

def results(symbol, start_date, end_date):
    rpy2.robjects.conversion.py2ri = numpy2ri
    a,b,c,d,e,f,g=stockdata27.stockdata(symbol, start_date, end_date)
    returns,Mu,Sigma=returns27.returns(g)
    MuA=numpy.array(Mu)
    SigmaA=numpy.array(Sigma)
    MuR = rpy2.robjects.conversion.py2ri(MuA)
    SigmaR=rpy2.robjects.conversion.py2ri(SigmaA)
    r_portfoliomv = rpy2.robjects.r['portfoliomv']
    resportfoliomv=r_portfoliomv(MuR,SigmaR)
    Mu_mv = resportfoliomv[0]
    sigma_mv = resportfoliomv[1]
    Theta_mv = resportfoliomv[2]
    Mu_mvA = numpy.squeeze(numpy.asarray(Mu_mv))
    Mu_mvL = numpy.array(Mu_mvA).tolist()
    Mu_mvjson = json.dumps(Mu_mvL)
    sigma_mvA = numpy.squeeze(numpy.asarray(sigma_mv))
    sigma_mvL = numpy.array(sigma_mvA).tolist()
    sigma_mvjson = json.dumps(sigma_mvL)
    Theta_mvA = numpy.squeeze(numpy.asarray(Theta_mv))
    Theta_mvL = numpy.array(Theta_mvA).tolist()
    Theta_mvjson = json.dumps(Theta_mvL)

    return Mu_mvjson, sigma_mvjson, Theta_mvjson

"""
import output
symbol = ['aapl','msft','yhoo','lyg','ba','bac','ge']
start_date = '20041201'
end_date = '20140731'
Mu_mv,sigma_mv,Theta_mv = output.results(symbol, start_date, end_date)
print(Mu_mv)
print(sigma_mv)
print(Theta_mv)

"""