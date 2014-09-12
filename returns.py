import numpy as np
import meancov as mc

def returns(X):

    t = len(X.T)
    lX = np.log(X)
    logXt = np.asmatrix(lX[:,1:t])
    logXt_1 = np.asmatrix(lX[:,0:t-1])
    rets = np.asmatrix(logXt - logXt_1)

    meanrets, covrets = mc.mean_cov(rets) 

    return rets, meanrets, covrets  