import timeit

import numpy as np

from ranking_2d import find_fair_ranking, query
from utils import read_file, score, polartoscalar

queries = []
for i in range(100):
    query_x = np.random.uniform(0, 500000)
    query_y = np.random.uniform(0, 16)
    queries.append([query_x, query_y])

ratios = [0.25, 0.5, 0.75, 1.0]
fractions = [0.2, 0.4, 0.6, 0.8, 1.0]
num_of_buckets_list = [100, 200, 300, 400, 500, 600, 700, 800, 1000]
datasets = ["adult",
            # "compas"
            ]
sensitive_attrs = ["sex", "Sex_Code_Text"]
columns = [["fnlwgt", "education-num"], ["RawScore", "DecileScore"]]
d = 2
flag = 0
for idx in range(len(datasets)):
    print("=================", datasets[idx], "=================")
    preprocessing_time = []
    query_times = []
    for frac in fractions:
        print("=================", "fraction:", frac, "=================")
        path = "real_data/" + datasets[idx] + "/" + datasets[idx] + "_f_" + str(frac) + ".csv"
        num_of_buckets = 100
        disparity, distribution, ranking, theta, duration = find_fair_ranking(path, columns[idx], sensitive_attrs[idx],
                                                                              num_of_buckets)
        preprocessing_time.append(duration)
        query_time = []
        dataset = read_file(path, columns[idx])
        f = polartoscalar([theta], d)
        scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])
        for q in queries:
            start = timeit.default_timer()
            query(q, f, scores, d, num_of_buckets)
            stop = timeit.default_timer()
            query_time.append(stop - start)
        query_times.append(np.mean(query_time))

    print("Varying dataset size:", preprocessing_time)
    print("Varying dataset size (query time):", query_times)

    preprocessing_time = []
    query_times = []
    for ratio in ratios:
        print("=================", "ratio:", ratio, "=================")
        path = "real_data/" + datasets[idx] + "/" + datasets[idx] + "_r_" + str(ratio) + ".csv"
        num_of_buckets = 100
        disparity, distribution, ranking, theta, duration = find_fair_ranking(path, columns[idx], sensitive_attrs[idx],
                                                                              num_of_buckets)
        preprocessing_time.append(duration)

        dataset = read_file(path, columns[idx])
        f = polartoscalar([theta], d)
        scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q, f, scores, d, num_of_buckets)
            stop = timeit.default_timer()
            query_time.append(stop - start)
        query_times.append(np.mean(query_time))

    print("Varying minority ratio:", preprocessing_time)
    print("Varying minority ratio (query time):", query_times)

    preprocessing_time = []
    query_times = []
    for num_of_buckets in num_of_buckets_list:
        print("=================", "number of buckets:", num_of_buckets, "=================")
        path = "real_data/" + datasets[idx] + "/" + datasets[idx] + "_r_0.25.csv"
        disparity, distribution, ranking, theta, duration = find_fair_ranking(path, columns[idx], sensitive_attrs[idx],
                                                                              num_of_buckets)
        preprocessing_time.append(duration)

        dataset = read_file(path, columns[idx])
        f = polartoscalar([theta], d)
        scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q, f, scores, d, num_of_buckets)
            stop = timeit.default_timer()
            query_time.append(stop - start)
        query_times.append(np.mean(query_time))

    print("Varying bucket size:", preprocessing_time)
    print("Varying bucket size (query time):", query_times)

# ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
# sizes = [1000, 10000, 100000, 1000000, 10000000]
# num_of_buckets = [10, 100, 1000, 10000, 100000]
#
# queries = []
# for i in range(100):
#     query_x = np.random.uniform(0, 1)
#     query_y = np.random.uniform(0, 1)
#     queries.append([query_x, query_y])
#
# preprocessing_time = []
# space = []
# query_times = []
# for size in sizes:
#     path = "synthetic_data/2d_sample_0.1_" + str(size) + ".csv"
#     num_of_buckets = 100
#     disparity, distribution, ranking, theta, duration = find_fair_ranking(path, ["X1", "X2"], "S", num_of_buckets)
#     preprocessing_time.append(duration)
#     space.append(len(ranking))
#     query_time = []
#     dataset = read_file(path, ["X1", "X2"])
#     d = 2
#     f = polartoscalar([theta], d)
#     scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])
#     for q in queries:
#         start = timeit.default_timer()
#         query(q, f, scores, d, num_of_buckets)
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
#     path = "synthetic_data/2d_sample_" + str(ratio) + "_10000.csv"
#     num_of_buckets = 100
#     disparity, distribution, ranking, theta, duration = find_fair_ranking(path, ["X1", "X2"], "S", num_of_buckets)
#     preprocessing_time.append(duration)
#     space.append(len(ranking))
#     query_time = []
#     dataset = read_file(path, ["X1", "X2"])
#     d = 2
#     f = polartoscalar([theta], d)
#     scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])
#     for q in queries:
#         start = timeit.default_timer()
#         query(q, f, scores, d, num_of_buckets)
#         stop = timeit.default_timer()
#         query_time.append(stop - start)
#     query_times.append(np.mean(query_time))
# print("Varying minority ratio:", preprocessing_time)
# print("Varying minority ratio (query time):", query_times)
# print("Varying minority ratio (space):", space)
#
# preprocessing_time = []
# space = []
# query_times = []
# for num_of_bucket in num_of_buckets:
#     path = "synthetic_data/2d_sample_0.1_10000.csv"
#     disparity, distribution, ranking, theta, duration = find_fair_ranking(path, ["X1", "X2"], "S", num_of_buckets)
#     preprocessing_time.append(duration)
#     space.append(len(ranking))
#     query_time = []
#     dataset = read_file(path, ["X1", "X2"])
#     d = 2
#     f = polartoscalar([theta], d)
#     scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])
#     for q in queries:
#         start = timeit.default_timer()
#         query(q, f, scores, d, num_of_buckets)
#         stop = timeit.default_timer()
#         query_time.append(stop - start)
#     query_times.append(np.mean(query_time))
# print("Varying bucket size:", preprocessing_time)
# print("Varying bucket size (query time):", query_times)
# print("Varying bucket size (space):", space)
