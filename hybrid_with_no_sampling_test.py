import timeit

import numpy as np
from hybrid_with_no_sampling import hybrid_with_no_sampling
from necklace_split_binary import query

queries = []
for i in range(100):
    query_x = np.random.uniform(0, 1)
    query_y = np.random.uniform(0, 1)
    queries.append([query_x, query_y])

ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
sizes = [1000, 10000, 100000, 1000000, 10000000]
num_of_buckets = [10, 100, 1000, 10000, 100000]

preprocessing_time = []
space = []
query_times = []
for size in sizes:
    path = "synthetic_data/2d_sample_0.1_" + str(size) + ".csv"
    num_of_buckets = 100
    num_of_cuts, boundary, hash_buckets, theta, duration = hybrid_with_no_sampling(path, "S", ["X1", "X2"], num_of_buckets)
    preprocessing_time.append(duration)
    space.append(len(boundary))
    query_time = []
    for q in queries:
        start = timeit.default_timer()
        query(q, boundary, hash_buckets,[theta])
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
    num_of_buckets = 100
    num_of_cuts, boundary, hash_buckets, theta, duration = hybrid_with_no_sampling(path, "S", ["X1", "X2"], num_of_buckets)
    preprocessing_time.append(duration)
    space.append(len(boundary))
    query_time = []
    for q in queries:
        start = timeit.default_timer()
        query(q, boundary, hash_buckets,[theta])
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
    path = "synthetic_data/2d_sample_0.1_1000000.csv"
    num_of_cuts, boundary, hash_buckets, theta, duration = hybrid_with_no_sampling(path, "S", ["X1", "X2"], num_of_buckets)
    preprocessing_time.append(duration)
    space.append(len(boundary))
    query_time = []
    for q in queries:
        start = timeit.default_timer()
        query(q, boundary, hash_buckets,[theta])
        stop = timeit.default_timer()
        query_time.append(stop - start)
    query_times.append(np.mean(query_time))
print("Varying bucket size:", preprocessing_time)
print("Varying bucket size (query time):", query_times)
print("Varying bucket size (space):", space)



# path = "synthetic_data/2d_sample_0.2_100.csv"
# number_of_buckets = 10
# num_of_cuts, boundary, hash_buckets, theta = hybrid_with_no_sampling(path, "S", ["X1", "X2"], number_of_buckets)
# print(queries[0])
# print(boundary)
# print(hash_buckets)
# print(query(queries[0], boundary, hash_buckets, [theta]))
