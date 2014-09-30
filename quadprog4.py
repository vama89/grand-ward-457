import numpy as np
from residuals import residuals
from steplength import steplength
from lusolve import lusolve

'''
Primal Objective: minimize    0.5 * (x.T * G * x) + g.T * x
                  subject to   A * x = b, C * x <= d

Dual Objective: L = 0.5 * (x.T * G * x) + g.T * x - mu * sum(log(s_i)) - y.T * ( A * x - b) - z.T ( C * x - s - d)

Use Mehrotra predictor-corrector algorithm to solve quadratic programming problem (Gertz and Wright 2001)

where 
    x is a n x 1 vector (minimization variable)
    y is a mA x 1 vector (Lagrange multiplier for equality constraint)
    z is a mC x 1 vector (Lagrange multiplier for inequality constraint)
    s is a mC x 1 vector (slackness condition)
    Q is a n x n positive definite matrix (Hessian/Covariance Matrix)
    c is a n x 1 vector (zero vector)
    C is a mC x n matrix (LHS of inequality constraints)
    d is a mC x 1 vector (RHS of inequality constraints)
    A is a mA x n matrix (LHS of equality constraints)
    b is a mA x 1 vector (RHS of equality constraints)

Optimality Conditions:
    G * x + g + A.T * y + C.T * z = 0
    A * x = b
    C * x + s = d
    (s,z) >= 0
    S * Z * e = 0

Note: This version is numerically stable, but slightly slower because we are using the non-reduced form.

By VC Analytics on 09/27/2014
'''

def qp(x, Q, c, C, d, A, b, maxiter):

    # Set leading dimension of A (number of equality constraints), C (number of inequality constraints), Q (number of assets)
    mA = len(A)
    mC = len(C)
    n = len(Q)

    # Initialize algorithm parameters: iteration count, tolerance level, step size, dampening, and centering power
    iter = 0
    eps = 1e-8
    alpha = 1
    eta = 0.99
    tau = 3

    # Initialize Lagrange multipliers, slackness condition, e, residuals, mu (complementary level), and sigma (centering level)
    y = np.ones((mA,1))
    z = np.ones((mC,1))
    s = np.ones((mC,1))
    e = np.ones((mC,1))
    rQ, rA, rC, rsz = residuals(x, y, z, s, Q, c, C, d, A, b)
    mu = np.dot(s.T,z)/mC
    sigma = 0.5

    while (iter<=maxiter and np.linalg.norm(rQ)>=eps and np.linalg.norm(rA)>=eps and np.linalg.norm(rC)>=eps and np.abs(mu)>=eps):

        # Set S, Z, S^(-1), Z^(-1) by diagonalizing s and z
        S = np.diag(s.T.flatten().tolist())
        Z = np.diag(z.T.flatten().tolist())
        Sinv = np.linalg.inv(S)
        Zinv = np.linalg.inv(Z)

        # Solve for dx_a, dy_a, dz_a, ds_a using LU decomposition/solver
        lhs = np.vstack(( np.hstack(( Q,-A.T,-C.T,np.zeros((n,mC)) )), \
        np.hstack(( A, np.zeros((mA,mA)), np.zeros((mA,mC)), np.zeros((mA,mC)) )), \
        np.hstack(( C, np.zeros((mC,mA)), np.zeros((mC,mC)), -np.eye(mC) )), \
        np.hstack(( np.zeros((mC,n)), np.zeros((mC,mA)), S, Z )) ))
        rhs = -np.vstack((rQ,rA,rC,rsz))
        dxyzs_a, L, U, P = lusolve(lhs,rhs)
        dx_a = dxyzs_a[0:n]
        dy_a = dxyzs_a[n:n+mA]
        dz_a = dxyzs_a[n+mA:n+mA+mC]
        ds_a = dxyzs_a[n+mA+mC:n+mA+mC+mC]

        # Compute alpha_a to be the largest value in (0,1] such that
        alpha_a, alphaz_a, alphas_a = steplength(z, s, dz_a, ds_a, eta)

        # Set mu_a and sigma_a
        mu_a = np.dot((z + alpha_a*dz_a).T,(s + alpha_a*ds_a))/mC
        sigma = (mu_a/mu)**tau

        # Solve system for dx, dy, dz, ds
        rsz = rsz - sigma*mu*e + dz_a*ds_a
        rhs = -np.vstack((rQ,rA,rC,rsz))
        dxyzs, L, U, P = lusolve(lhs,rhs)
        dx = dxyzs[0:n]
        dy = dxyzs[n:n+mA]
        dz = dxyzs[n+mA:n+mA+mC]
        ds = dxyzs[n+mA+mC:n+mA+mC+mC]

        # Compute alpha to be the largest value in (0,1] such that
        alpha, alphaz, alphas = steplength(z, s, dz, ds, eta)

        # Update x, z, s, rQ, rA, rC, rsz, and mu
        x = x + alpha*dx
        y = y + alpha*dy
        z = z + alpha*dz
        s = s + alpha*ds
        rQ, rA, rC, rsz = residuals(x, y, z, s, Q, c, C, d, A, b)
        mu = np.dot(s.T,z)/mC

        # Iteration count
        iter = iter + 1

    xstar = x
    ystar = y
    zstar = z
    sstar = s

    return xstar, ystar, zstar, sstar