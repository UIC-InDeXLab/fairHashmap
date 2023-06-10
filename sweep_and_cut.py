import timeit

import numpy as np
import pandas as pd
from bisect import bisect


def sweep_and_cut(path, column, sens_attr, num_of_buckets):
    df = pd.read_csv(path)
    start = timeit.default_timer()
    df = df.sort_values(column)
    t = df[column].values
    G = df[sens_attr].values
    G_unique, G_count = np.unique(df[sens_attr].values, return_counts=True)
    n = df.shape[0]
    C = np.zeros(len(G_unique), dtype=int)
    w = np.zeros(n, dtype=int)
    for i in range(n):
        g = np.where(G_unique == G[i])[0][0]
        w[i] = (C[g] // (G_count[g] / num_of_buckets)) + 1
        C[g] += 1
    hash_buckets = []
    boundary = []
    i = 0
    while True:
        while i < n - 1 and w[i] == w[i + 1]:
            i += 1
        if i == n - 1:
            break
        hash_buckets.append(w[i])
        boundary.append((t[i] + t[i + 1]) / 2)
        if i == n - 2:
            hash_buckets.append(w[i])
            boundary.append(t[i])
            break
        i += 1
    stop = timeit.default_timer()
    return boundary, hash_buckets, stop - start


def query(q, boundary, hash_buckets):
    return hash_buckets[bisect(boundary, q)]


