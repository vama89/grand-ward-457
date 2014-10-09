import numpy

"""
Computes components of the parameters of the portfolio using MLE
techniques--Mu and Sigma. (Stambaugh 1997)
Note: Adds onto stockdata27.py

-----Input-----
X: Matrix of return data, excluding the return data being estimated
Y: Matrix of the return data being estimated
ET: Vector of estimated Mu, excluding the mean return being estimated
V: Covariance matrix component used to estimate Mu and Sigma
nidx: indexing the sorted data

-----Output----
C: list of estimated parameters
E2: estimated component for Mu
Sigma2: variance of the residuals
Vnew: estimated component of Sigma

Written by: VC Analytics 10/6/2014
"""

def mle2(X,Y,ET,V,nidx):

    n = len(X)
    bar1 = numpy.ones((n,1))
    X = numpy.hstack((bar1,X))  
    C = numpy.squeeze(numpy.dot(numpy.linalg.inv(numpy.dot(X.T,X)),numpy.dot(X.T,Y))).tolist()
    B = numpy.matrix(C[nidx:])
    A = numpy.matrix(C[:nidx])

    YM = numpy.asmatrix(Y)
    XM = numpy.asmatrix(X)
    CM = numpy.asmatrix(C).T

    E2 = A + numpy.dot(B,ET)
    res = YM-numpy.dot(XM,CM)
    Sigma2 = [numpy.squeeze(numpy.array(numpy.dot(res.T,res))).tolist()]
    V11 = V
    V12 = numpy.dot(V11,B.T)
    V21 = V12.T
    V22 = Sigma2 + numpy.dot(numpy.dot(B,V11),B.T)
    Vnew = numpy.vstack((numpy.hstack((V11,V12)),numpy.hstack((V21,V22))))

    return C, E2, Sigma2, Vnew