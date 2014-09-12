
import rpy2.robjects
import json
import numpy

rpy2.robjects.r('''

		portfoliomv <- function(mu, sigma) {

		# Computes the minimum variance portfolio. The investor prefers a portfolio
		# with the least amount of risk and is not concern about the portfolio's
		# expected return
				
			n          <- nrow(mu)
			bar1       <- matrix(1,n,1)
			
		# H Matrix Elements			
			aa   <- t(mu)%*%solve(sigma)%*%mu
			bb   <- t(mu)%*%solve(sigma)%*%bar1
			cc   <- t(bar1)%*%solve(sigma)%*%bar1
			dd   <- aa * cc - bb ^ 2
			
		# Minimum Variance Portfolio
			mu_mv      <- bb/cc
			sigma_mv   <- cc^(-1)
			ssigma_mv  <- sigma_mv^0.5
			theta_mv   <- solve(sigma)%*%bar1%*%sigma_mv
			
		# Results
			result <- list(mu_mv=mu_mv, ssigma_mv=ssigma_mv, theta_mv=theta_mv)
			return(result)
			
		}
		''')
"""
# Copy and paste script into terminal
# Define Mu = robjects.r['matrix'](1,3,1), Sigma = robjects.r['diag'](1,3)
# Define the R function as r_portfoliomv = robjects.r['portfoliomv']
# Execute as resportfoliomv = r_portfoliomv(Mu,Sigma)
# mu_mv = resportfoliomv[0]
# sigma_mv = resportfoliomv[1]
# theta_mv = resportfoliomv[2]
# mu_mvarray = np.squeeze(np.asarray(mu_mv))
# mu_mvlst = np.array(mu_mvarray).tolist()
# mu_mvjson = json.dumps(mu_mvlst)
# sigma_mvarray = np.squeeze(np.asarray(sigma_mv))
# sigma_mvlst = np.array(sigma_mvarray).tolist()
# sigma_mvjson = json.dumps(sigma_mvlst)
# theta_mvarray = np.squeeze(np.asarray(theta_mv))
# theta_mvlst = np.array(theta_mvarray).tolist()
# theta_mvjson = json.dumps(theta_mvlst)
"""