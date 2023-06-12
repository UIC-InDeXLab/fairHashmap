import math
import random
import numpy as np
import pandas as pd


def generate_2D_data(file_name, n, minority_count):
    majority_count = n - minority_count
    df = pd.DataFrame(np.random.uniform(0, 1, size=(n, 2)), columns=["X1", "X2"])
    s = []
    for i in range(minority_count):
        s.append("F")
    for i in range(majority_count):
        s.append("M")
    random.shuffle(s)
    df["S"] = s
    df.to_csv("synthetic_data/" + file_name)


def score(t, f, d):
    c = 0
    if len(f) != d:
        print('Error: Function length should be equal to d')
        return
    for j in range(d):
        c += f[j] * t[j]
    return c


def rank(dataset, theta, d):
    f = polartoscalar(theta, d)
    r = sorted([[i, score(dataset[i], f, d)] for i in range(len(dataset))], key=lambda x: x[1], reverse=True)
    return tuple([r[i][0] for i in range(len(r))])


def polartoscalar(theta, d, r=1):
    f = []
    for j in range(d - 1, 0, -1):
        f.insert(0, r * math.sin(theta[j - 1]))
        r *= math.cos(theta[j - 1])
    f.insert(0, r)
    return f


def read_file(file, columns):
    dataset = pd.read_csv(file)
    n = dataset.shape[0]
    d = 2
    dataset = dataset[[col for col in columns]]
    dataset["idx"] = [float(i) for i in range(dataset.shape[0])]
    dataset = dataset.to_numpy()
    return dataset
