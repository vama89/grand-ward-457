import json
import numpy
import quadprog4

"""
Computes the minimium variance portfolio with short-selling and without short-selling.

By VC Analytics on 09/27/2014
"""

def portfoliomv(Mu, Sigma):

    """
    Computes the minimum variance portfolio. The investor prefers a portfolio
    with the least amount of risk and is not concern about the portfolio's
    expected return
    """

    n = len(Mu)
    bar1 = numpy.asmatrix(numpy.ones(n)).T
			
    #H Matrix Elements			
    aa = numpy.dot(numpy.dot(Mu.T,Sigma.I),Mu)
    bb = numpy.dot(numpy.dot(Mu.T,Sigma.I),bar1)
    cc = numpy.dot(numpy.dot(bar1.T,Sigma.I),bar1)
    dd = aa * cc - bb ** 2
			
    # Minimum Variance Portfolio
    Mu_mv = bb/cc
    Sigma_mv = cc.I
    sigma_mv = numpy.sqrt(Sigma_mv)
    Theta_mv = numpy.dot(numpy.dot(Sigma.I,bar1),Sigma_mv)

    Mu_mvjson = json.dumps(numpy.squeeze(numpy.asarray(Mu_mv)).tolist())
    sigma_mvjson = json.dumps(numpy.squeeze(numpy.asarray(sigma_mv)).tolist())	
    Theta_mvjson = json.dumps(numpy.squeeze(numpy.asarray(Theta_mv)).tolist())
	
    # Results
    return Mu_mvjson, sigma_mvjson, Theta_mvjson

def portfoliomvns(Mu, Sigma):

    """
    Computes the minimum variance portfolio with no short-selling. The investor prefers a portfolio
    with the least amount of risk and is not concern about the portfolio's
    expected return
    """

    n = len(Mu)

    # Solve minimum variance portfolio with no short-selling using a quadratic programming algorithm
    Q = numpy.asarray(Sigma)
    c = numpy.zeros((n,1))
    C = numpy.vstack((numpy.eye(n),-numpy.eye(n)))
    d = numpy.vstack((numpy.zeros((n,1)),-numpy.ones((n,1))))
    A = numpy.ones((1,n))
    b = 1.0
    x = numpy.zeros((n,1))
    maxiter = 200
    xstar, ystar, zstar, sstar = quadprog4.qp(x, Q, c, C, d, A, b, maxiter)

    # Minimum Variance Portfolio
    Theta_mvns = xstar
    Mu_mvns = numpy.dot(Mu.T,Theta_mvns)
    sigma_mvns = numpy.sqrt(( numpy.dot(numpy.dot(Theta_mvns.T,Sigma),Theta_mvns) )[0])

    Mu_mvnsjson = json.dumps(numpy.squeeze(numpy.asarray(Mu_mvns)).tolist())
    sigma_mvnsjson = json.dumps(numpy.squeeze(numpy.asarray(sigma_mvns)).tolist())	
    Theta_mvnsjson = json.dumps(numpy.squeeze(numpy.asarray(Theta_mvns)).tolist())

    # Results
    return Mu_mvnsjson, sigma_mvnsjson, Theta_mvnsjson