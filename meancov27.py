import numpy

def mean_cov(x):
    """
    Computes the mean and the covariance of x
    By VC Analytics on 09/27/2014
    """	

    mu = numpy.asmatrix(numpy.mean(x,axis=1))
    cov = numpy.asmatrix(numpy.cov(x))

    return mu, cov