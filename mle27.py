import sorting27
import returns27
import meancov27
import stockdata27
import mle227
import numpy

"""
Computes the required parameters for portfolio analysis--Mu and Sigma--
for different lengths of financial time-series data. First, it sorts
the data, then it computes the portfolio parameters. (Stambaugh 1997)
Note: Adds onto stockdata27.py

-----Input----
symbol: vector of symbols
start_date: earliest data point collected
end_date: latest data point collected

----Output----
date: list of dates for each stock 
open: adjusted open price
high: adjusted high price
low: adjusted low price
close: adjusted close price 
vol: volume of stock traded
adjclose: adjusted close price
adjclosesort: adjusted sorted close price
symbolsort: sorted stock symbols
Mu: vector of mean returns for each stock
Sigma: covariance matrix of returns

Written by: VC Analytics 10/6/2014
"""

def mle(symbol, start_date, end_date):

    date, open, high, low, close, vol, adjclose = stockdata27.stockdata(symbol, start_date, end_date)
    adjclosesort, symbolsort = sorting27.sorting(adjclose, symbol)

    # Initialize
    n = len(adjclosesort)

    R = []
    Rtemp = []
    E = []
    L = []
    C = []
    ES = []
    ET = []
    Sigmahat = []
    Lboo = []
    nidx = 0

    for i in range(n):
        rettemp, ertemp, ctemp = returns27.returns(numpy.array(adjclosesort[i]))
        Rtemp.append(numpy.squeeze(numpy.asarray(rettemp)).tolist())
        E.append(numpy.squeeze(numpy.asarray(ertemp)).tolist())
        L.append(len(Rtemp[i]))

    maxL = max(L)
    LD = numpy.array(maxL) - numpy.array(L)
    for i in range(n):
        zeros = [0]*LD[i]
        Rtemp1 = zeros + Rtemp[i]
        R.append(Rtemp1)

    for j in range(n):
        Lbootemp = (L[j] == maxL) + 0
        Lboo.append(Lbootemp)

    lba = numpy.array(Lboo)
    lbaidx = lba.nonzero()[0].tolist()
    lbas = lbaidx[0]
    lbae = lbaidx[-1]+1
    R1 = R[lbas:lbae]
    E1, V11 = meancov27.mean_cov(R1) 
    Ehat = E1
    nidx = nidx + len(lbaidx)

    # Compute Mu and Sigma
    for j in xrange(1,n):
        if n <= nidx:
            break
        Lboo = [ ]
        Ltemp = L[nidx:]
        maxLtemp = max(Ltemp)
        nstart = maxL - maxLtemp
        for i in range(n):
            Lbootemp = (L[i] == maxLtemp) + 0
            Lboo.append(Lbootemp)
        LbooA = numpy.array(Lboo)
        idxtemp = numpy.where(LbooA!=0)
        idxtemp = idxtemp[0]
        nidxtemp = len(idxtemp)
        ET1 = numpy.array(E[0:idxtemp[0]])
        ET1mat = numpy.matrix(ET1).T
        Rs  = [ ]
        for k in range(idxtemp[0]):
            Rs.append(R[k][nstart:])
        Rs1 = numpy.array(Rs).T
        Es1 = numpy.mean(Rs,axis=1)
        Rs2 = [ ]
        for t in range(len(idxtemp)):
            Rs2temp = R[idxtemp[t]][nstart:]
            Rs2.append(Rs2temp)
        Y = numpy.array(Rs2).T
        Ctemp, E2, Sigma2hat, Vtemp = mle227.mle2(Rs1,Y,ET1mat,V11,nidxtemp)
        Ehat = numpy.hstack((Ehat,E2))
        Sigmahat = Sigmahat + Sigma2hat
        V11 = Vtemp
        ET.append(ET1.tolist())
        ES.append(Es1.tolist())
        C.append(Ctemp)
        nidx = nidx + len(idxtemp)

    Sigma = V11
    Mu = Ehat.T
    ret = Rtemp

    return date, open, high, low, close, vol, adjclose, adjclosesort, symbolsort, ret, Mu, Sigma