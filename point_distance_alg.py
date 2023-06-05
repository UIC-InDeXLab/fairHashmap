import timeit

import numpy as np
import pandas as pd
from bisect import bisect


def preprocessing(path, col, sens_attr, num_of_buckets):
    df = pd.read_csv(path)
    start = timeit.default_timer()
    df = df.sort_values(col)
    t = df[col].values
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


ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
sizes = [1000, 10000, 100000, 1000000, 10000000]
num_of_buckets = [10, 100, 1000, 10000, 100000]
queries = list(np.random.uniform(0, 1, 100))

preprocessing_time = []
space = []
query_times = []
# for size in sizes:
#     boundary, hash_buckets, duration = preprocessing("data/2d_sample_0.1_" + str(size) + ".csv", "X1", "S", 100)
#     preprocessing_time.append(duration)
#     space.append(len(boundary))
#     query_time = []
#     for q in queries:
#         start = timeit.default_timer()
#         query(q, boundary, hash_buckets)
#         stop = timeit.default_timer()
#         query_time.append(stop - start)
#     query_times.append(np.mean(query_time))
# print("Varying dataset size:", preprocessing_time)
# print("Varying dataset size (query time):", query_times)
# print("Varying dataset size (space):", space)

preprocessing_time = []
space = []
query_times = []
for ratio in ratios:
    boundary, hash_buckets, duration = preprocessing("data/2d_sample_" + str(ratio) + "_1000000.csv", "X1", "S", 100)
    preprocessing_time.append(duration)
    space.append(len(boundary))
    query_time = []
    for q in queries:
        start = timeit.default_timer()
        query(q, boundary, hash_buckets)
        stop = timeit.default_timer()
        query_time.append(stop - start)
    query_times.append(np.mean(query_time))

print("Varying minority ratio:", preprocessing_time)
print("Varying minority ratio (query time):", query_times)
print("Varying minority ratio (space):", space)

preprocessing_time = []
space = []
query_times = []
for num_of_bucket in num_of_buckets:
    boundary, hash_buckets, duration = preprocessing("data/2d_sample_0.1_1000000.csv", "X1", "S", num_of_bucket)
    preprocessing_time.append(duration)
    space.append(len(boundary))
    query_time = []
    for q in queries:
        start = timeit.default_timer()
        query(q, boundary, hash_buckets)
        stop = timeit.default_timer()
        query_time.append(stop - start)
    query_times.append(np.mean(query_time))

print("Varying bucket size:", preprocessing_time)
print("Varying bucket size (query time):", query_times)
print("Varying bucket size (space):", space)
