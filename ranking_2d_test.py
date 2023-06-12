import timeit

import numpy as np

from ranking_2d import find_fair_ranking, query
from utils import read_file, score, polartoscalar

ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
sizes = [1000, 10000, 100000, 1000000, 10000000]
num_of_buckets = [10, 100, 1000, 10000, 100000]

queries = []
for i in range(100):
    query_x = np.random.uniform(0, 1)
    query_y = np.random.uniform(0, 1)
    queries.append([query_x, query_y])

# preprocessing_time = []
# space = []
# query_times = []
# for size in sizes:
#     path = "synthetic_data/2d_sample_0.1_" + str(size) + ".csv"
#     num_of_buckets = 100
#     disparity, distribution, ranking, duration = find_fair_ranking(path, ["X1", "X2"], "S", num_of_buckets)
#     preprocessing_time.append(duration)
#     space.append(len(ranking))
#     query_time = []
#     for q in queries:
#         start = timeit.default_timer()
#         query(q)
#         stop = timeit.default_timer()
#         query_time.append(stop - start)
#     query_times.append(np.mean(query_time))
# print("Varying dataset size:", preprocessing_time)
# print("Varying dataset size (query time):", query_times)
# print("Varying dataset size (space):", space)
#
# preprocessing_time = []
# space = []
# query_times = []
# for ratio in ratios:
#     path = "synthetic_data/2d_sample_"+str(ratio) + "_10000.csv"
#     num_of_buckets = 100
#     disparity, distribution, ranking, duration = find_fair_ranking(path, ["X1", "X2"], "S", num_of_buckets)
#     preprocessing_time.append(duration)
#     space.append(len(ranking))
#     query_time = []
#     for q in queries:
#         start = timeit.default_timer()
#         query(q)
#         stop = timeit.default_timer()
#         query_time.append(stop - start)
#     query_times.append(np.mean(query_time))
# print("Varying minority ratio:", preprocessing_time)
# print("Varying minority ratio (query time):", query_times)
# print("Varying minority ratio (space):", space)

# preprocessing_time = []
# space = []
# query_times = []
# for num_of_bucket in num_of_buckets:
#     path = "synthetic_data/2d_sample_0.1_10000.csv"
#     disparity, distribution, ranking, duration = find_fair_ranking(path, ["X1", "X2"], "S", num_of_buckets)
#     preprocessing_time.append(duration)
#     space.append(len(ranking))
#     query_time = []
#     for q in queries:
#         start = timeit.default_timer()
#         query(q)
#         stop = timeit.default_timer()
#         query_time.append(stop - start)
#     query_times.append(np.mean(query_time))
# print("Varying bucket size:", preprocessing_time)
# print("Varying bucket size (query time):", query_times)
# print("Varying bucket size (space):", space)


path = "synthetic_data/2d_sample_0.2_100.csv"
disparity, distribution, ranking, theta, duration = find_fair_ranking(path, ["X1", "X2"], "S", 20)

dataset = read_file(path,["X1", "X2"])
d = 2
f = polartoscalar([theta], d)
scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])

print(query(queries[0], f, scores, 2, 20))
