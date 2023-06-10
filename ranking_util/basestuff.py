import math
import pandas as pd

n = None
d = None
dataset = None


def read_file(file, columns):
    global dataset, n, d
    dataset = pd.read_csv(file)
    n = dataset.shape[0]
    d = 2
    dataset = dataset[[col for col in columns]]
    dataset["idx"] = [float(i) for i in range(dataset.shape[0])]
    dataset = dataset.to_numpy()


def read_df(dataframe, columns):
    global dataset, n, d
    dataset = dataframe[[col for col in columns]]
    n = dataset.shape[0]
    d = 2
    dataset["idx"] = [float(i) for i in range(dataset.shape[0])]
    dataset = dataset.to_numpy()


def score(i, f):
    c = 0
    if len(f) != d:
        print('Error: Function length should be equal to d')
        return
    for j in range(d):
        c += f[j] * dataset[i, j]
    return c


def rank(input, isweight=True):
    f = polartoscalar(input) if not isweight else input
    r = sorted([[i, score(i, f)] for i in range(n)], key=lambda x: x[1], reverse=True)
    return tuple([r[i][0] for i in range(len(r))])


def polartoscalar(theta, r=1):
    f = []
    for j in range(d - 1, 0, -1):
        f.insert(0, r * math.sin(theta[j - 1]))
        r *= math.cos(theta[j - 1])
    f.insert(0, r)
    return f
