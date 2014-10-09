import numpy

"""
Sorts the data from longest time-series to shortest times-series.
This is to help compute the paramters for the portfolio. (Stambaugh 1997)
Note: Adds onto stockdata27.py

-----Input-----
X: data matrix
label: label attached to Xsort

-----Output----
Xsort: sorted data matrix, X
labelsort: sorted label vector

Written by: VC Analytics 10/6/2014
"""

def sorting(X, label):

    n = len(X)
    l = [ ]
    lboo = [ ]
    Xsort = [ ]
    labelsort = [ ]

    for j in range(n):
        Ltemp = len(X[j])
        l.append(Ltemp)

    for k in range(n):
        maxl = max(l)
        for i in range(n):
            lbootemp = (l[i] == maxl) + 0
            lboo.append(lbootemp)
        lba = numpy.array(lboo)
        lbaidx = lba.nonzero()[0].tolist()
        for i in lbaidx:
            labelsort.append(label[i])
            Xsort.append(X[i])
            l[i] = 0
        lboo = [ ]
        if all(v == 0 for v in l):
            break

    return Xsort, labelsort