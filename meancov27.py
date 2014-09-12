import numpy

def mean_cov(x):
    mu = numpy.mean(x,axis=1)
    cov = numpy.asmatrix(numpy.cov(x))

    return mu, cov