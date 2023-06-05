# Abolfazl Asudeh Oct. 2017
# http://asudeh.github.io
import math
from heapq import heappush, heappop, heapify

import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------------
# def mylog(st, outputfile):
#     outfile = open(outputfile, 'a')
#     outfile.write(st + '\n')
#     outfile.close()


# -----------------------------------------------------------------------------------
n = None  # database size
d = None  # number of attributes (|D|)
D = None
dataset = None  # type numpy:ndarray; original set of points (all tuples)
dataset_unique = None
debugmod = 'on'  # type string; turns the debug mode on and off
TupleNames = None
dataset_ = None
n_ = None


def setparams(numberofTuples, numberofAttributes, debug='on'):
    global n, d, D, debugmod
    n = numberofTuples
    d = numberofAttributes
    D = [i for i in range(d)]
    debugmod = debug


def unique(x):
    y = np.ascontiguousarray(x).view(np.dtype((np.void, x.dtype.itemsize * x.shape[1])))
    _, idx = np.unique(y, return_index=True)
    return x[idx]


def genData(file=None, pythonfile=True, header=0, delim=',', cols=(1, 2, 3),
            tuplenames=None):  # the last column should be the protected column
    global dataset, fairportion, dataset_unique, TupleNames
    print('started generating/loading the data')
    if file is None:
        dataset = np.random.rand(n, d)
        dataset = np.append(dataset, np.random.randint(low=0, high=2, size=n).reshape(n, 1), axis=1)
    elif pythonfile:
        dataset = np.load(file)
    else:
        dataset = np.genfromtxt(file, delimiter=delim, skip_header=header, usecols=cols)  # , max_rows=n);
        if tuplenames is not None:
            TupleNames = np.genfromtxt(file, delimiter=delim, skip_header=header, usecols=[0], names=True, dtype=None,
                                       encoding=None)
    dataset = np.append(dataset[0:n, 0:d], np.array([i for i in range(n)]).reshape(n, 1), 1)
    dataset_unique = unique(dataset[0:n, 0:d])


def genDataDf(df):
    global dataset
    n = df.shape[0]
    df['IDX'] = [i for i in range(n)]
    dataset = df[['X1', 'X2', 'IDX']].values


def genDataDf_(path):
    global dataset_, n_
    df = pd.read_csv(path)
    n_ = df.shape[0]
    df['IDX'] = [i for i in range(n_)]
    dataset_ = df[['X1', 'X2', 'IDX']].values


def score(i, f):
    c = 0
    if len(f) != d:
        print('Error: Function length should be equal to d')
        return
    for j in range(d):
        c += f[j] * dataset[i, j]
    return c


def score_(i, f):
    c = 0
    if len(f) != d:
        print('Error: Function length should be equal to d')
        return
    for j in range(d):
        c += f[j] * dataset_[i, j]
    return c


# def top_k(input, k=10, isweight=True):
#     f = polartoscalar(input) if not isweight else input
#     heap = [[score(i, f), i] for i in range(k)]
#     heapify(heap)  # test to be minheap
#     for i in range(k, n):
#         s = score(i, f)
#         if s > heap[0][0]:
#             heappop(heap)
#             heappush(heap, [s, i])
#     return frozenset([heap[i][1] for i in range(k)])


def rank(input, isweight=True):
    f = polartoscalar(input) if not isweight else input
    r = sorted([[i, score(i, f)] for i in range(n)], key=lambda x: x[1], reverse=True)
    r_ = sorted([[i, score_(i, f)] for i in range(n_)], key=lambda x: x[1], reverse=True)
    return tuple([r[i][0] for i in range(len(r))]), tuple([r_[i][0] for i in range(len(r_))])


def polartoscalar(theta, r=1):
    f = []
    # if len(theta)==1: return [math.cos(theta[0]), math.sin(theta[0])]
    for j in range(d - 1, 0, -1):
        f.insert(0, r * math.sin(theta[j - 1]))
        r *= math.cos(theta[j - 1])
    f.insert(0, r)
    return f

# def myHash(input):
#     return input
#
#
# def scolartopolar(f, m=None):  # test it
#     if m is None:
#         m = d
#     theta = []
#     cumulative = f[0] * f[0]
#     for i in range(1, m):
#         theta.append(np.arctan2(f[i], f[i - 1] / math.fabs(f[i - 1]) * math.sqrt(cumulative)))
#         cumulative += f[i] * f[i]
#     return (math.sqrt(cumulative), theta)  # (r,theta)
#
#
# def angledist(th, thp):
#     x = polartoscalar(th)
#     y = polartoscalar(thp)
#     return sum([x[i] * y[i] for i in range(len(x))])
