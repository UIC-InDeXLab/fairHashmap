import timeit
import numpy as np
from necklace_split_binary import necklace_split, query

ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
sizes = [1000, 10000, 100000, 1000000, 10000000]
num_of_buckets = [10, 100, 1000, 10000, 100000]
queries = list(np.random.uniform(0, 1, 100))

preprocessing_time = []
space = []
query_times = []
for size in sizes:
    path = "synthetic_data/2d_sample_0.1_" + str(size) + ".csv"
    _, boundary, hash_buckets, duration = necklace_split(path, "X1", "S", 100)
    preprocessing_time.append(duration)
    space.append(len(boundary))
    query_time = []
    for q in queries:
        start = timeit.default_timer()
        query(q, boundary, hash_buckets)
        stop = timeit.default_timer()
        query_time.append(stop - start)
    query_times.append(np.mean(query_time))
print("Varying dataset size:", preprocessing_time)
print("Varying dataset size (query time):", query_times)
print("Varying dataset size (space):", space)

preprocessing_time = []
space = []
query_times = []
for ratio in ratios:
    path = "synthetic_data/2d_sample_" + str(ratio) + "_10000.csv"
    _, boundary, hash_buckets, duration = necklace_split(path, "X1", "S", 100)
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
    path = "synthetic_data/2d_sample_0.1_10000.csv"
    _, boundary, hash_buckets, duration = necklace_split(path, "X1", "S", num_of_bucket)
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
