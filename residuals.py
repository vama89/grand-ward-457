import numpy as np

"""
F(x,y,z,s) = residuals, which determines J(x,y,z,s) * dX = -residuals 
By VC Analytics on 09/27/2014
"""

def residuals(x, y, z, s, Q, c, C, d, A, b):

    n = len(x)
    mC = len(C)
    mA = len(A)
    S = np.diag(s.T.flatten().tolist())
    Z = np.diag(z.T.flatten().tolist())
    e = np.ones((mC,1))

    rQ = np.dot(Q,x) + c - np.dot(A.T,y) - np.dot(C.T,z)
    rA = np.dot(A,x) - b
    rC = np.dot(C,x) - s - d
    rsz = np.dot(np.dot(Z,S),e)

    return rQ, rA, rC, rsz