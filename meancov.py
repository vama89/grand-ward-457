import numpy as np

def mean_cov(x):
    mu = np.mean(x,axis=1)
    cov = np.asmatrix(np.cov(x))

    return mu, cov