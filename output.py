import stockdata as sd
import returns as ret
import portfoliomv
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects.numpy2ri import numpy2ri
import json

def results(symbol, start_date, end_date):
    ro.conversion.py2ri = numpy2ri
    a,b,c,d,e,f,g=sd.stockdata(symbol, start_date, end_date)
    returns,Mu,Sigma=ret.returns(g)
    MuA=np.array(Mu)
    SigmaA=np.array(Sigma)
    MuR = ro.conversion.py2ri(MuA)
    SigmaR=ro.conversion.py2ri(SigmaA)
    r_portfoliomv = ro.r['portfoliomv']
    resportfoliomv=r_portfoliomv(MuR,SigmaR)
    Mu_mv = resportfoliomv[0]
    sigma_mv = resportfoliomv[1]
    Theta_mv = resportfoliomv[2]
    Mu_mvA = np.squeeze(np.asarray(Mu_mv))
    Mu_mvL = np.array(Mu_mvA).tolist()
    Mu_mvjson = json.dumps(Mu_mvL)
    sigma_mvA = np.squeeze(np.asarray(sigma_mv))
    sigma_mvL = np.array(sigma_mvA).tolist()
    sigma_mvjson = json.dumps(sigma_mvL)
    Theta_mvA = np.squeeze(np.asarray(Theta_mv))
    Theta_mvL = np.array(Theta_mvA).tolist()
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