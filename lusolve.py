from lu_decomposition import lu_decomposition
import numpy as np

"""
Solve A * x = b using LU Decomposition
    1. Forward substitution: L * y = P * b 
    2. backward substitution: U * x = y

By VC Analytics on 09/27/2014
"""

def lusolve(A,b):

    L, U, P= lu_decomposition(A)
    L = np.array(L)
    U = np.array(U)
    P = np.array(P)
    y = np.linalg.solve(L,np.dot(P,b))
    x = np.linalg.solve(U,y)

    return x, L, U, P