import json
import numpy

def portfoliomv(Mu, Sigma):

    """
    Computes the minimum variance portfolio. The investor prefers a portfolio
    with the least amount of risk and is not concern about the portfolio's
    expected return
    """

    n = len(Mu)
    bar1 = numpy.asmatrix(numpy.ones(n)).T
			
    #H Matrix Elements			
    aa = Mu.T * Sigma.I * Mu
    bb = Mu.T * Sigma.I * bar1
    cc = bar1.T * Sigma.I * bar1
    dd = aa * cc - bb ** 2
			
    # Minimum Variance Portfolio
    Mu_mv = bb/cc
    Sigma_mv = cc ** (-1)
    sigma_mv = numpy.sqrt(Sigma_mv)
    Theta_mv = Sigma.I * bar1 * Sigma_mv

    Mu_mvjson = json.dumps(numpy.squeeze(numpy.asarray(Mu_mv)).tolist())
    sigma_mvjson = json.dumps(numpy.squeeze(numpy.asarray(sigma_mv)).tolist())	
    Theta_mvjson = json.dumps(numpy.squeeze(numpy.asarray(Theta_mv)).tolist())
	
    # Results
    return Mu_mvjson, sigma_mvjson, Theta_mvjson