import numpy
import meancov27

def returns(X):

    t = len(X.T)
    n = len(X)
    if n == t:
        lX = numpy.log(X)
        logXt = numpy.asmatrix(lX[1:t])
        logXt_1 = numpy.asmatrix(lX[0:t-1])
        rets = numpy.asmatrix(logXt - logXt_1)
    else:
        lX = numpy.log(X)
        logXt = numpy.asmatrix(lX[:,1:t])
        logXt_1 = numpy.asmatrix(lX[:,0:t-1])
        rets = numpy.asmatrix(logXt - logXt_1)

    meanrets, covrets = meancov27.mean_cov(rets) 

    return rets, meanrets, covrets  