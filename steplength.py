
"""
Determines the step length of the Mehrotra predictor-corrector algorithm.

By VC Analytics on 09/27/2014 ported from Wright Matlab Code
"""

def steplength(z, s, dz, ds, eta):

    #Given the current iterate (z,s) and steps (dx,ds). Compute the step
    #lengths that ensure that z + alphaz * dz > 0 and s + alphas*ds>0, and
    #alpha = min(alphax,alphas). eta indicates the maximum fraction of
    #step to the boundary
    alphaz = -1/min(min(dz/z),-1)
    alphaz = min(1,eta*alphaz)
    alphas = -1/min(min(ds/s),-1)
    alphas = min(1,eta*alphas)
    alpha = min(alphaz,alphas)

    return alpha, alphaz, alphas