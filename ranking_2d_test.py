import timeit

import numpy as np

from ranking_2d import find_fair_ranking, query
from utils import read_file, score, polartoscalar, plot

queries = []
for i in range(1000):
    query_x = np.random.uniform(0, 100000)
    query_y = np.random.uniform(0, 100000)
    queries.append([query_x, query_y])

ratios = [0.25, 0.5, 0.75, 1.0]
fractions = [0.2, 0.4, 0.6, 0.8, 1.0]
num_of_buckets_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
datasets = ["adult", "compas"]
sensitive_attrs = ["sex", "Sex_Code_Text"]
columns = [["fnlwgt", "education-num"], ["Person_ID", "Case_ID"]]
d = 2
flag = 0
for idx in range(len(datasets)):
    print("=================", datasets[idx], "=================")
    preprocessing_time = []
    query_times = []
    for frac in fractions:
        print("=================", "fraction:", frac, "=================")
        path = (
            "real_data/"
            + datasets[idx]
            + "/"
            + datasets[idx]
            + "_f_"
            + str(frac)
            + ".csv"
        )
        num_of_buckets = 100
        disparity, distribution, ranking, theta, duration = find_fair_ranking(
            path, columns[idx], sensitive_attrs[idx], num_of_buckets
        )
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

    print("Varying dataset size (prep time):", preprocessing_time)
    print("Varying dataset size (query time):", query_times)
    plot(
        "plots/ranking_2d/" + datasets[idx] + "/varying_size_prep_time.png",
        fractions,
        preprocessing_time,
        fractions,
        "Varying dataset size (prep time)",
        "Fraction",
        "Time (sec)",
    )
    plot(
        "plots/ranking_2d/" + datasets[idx] + "/varying_size_query_time.png",
        fractions,
        query_times,
        fractions,
        "Varying dataset size (query time)",
        "Fraction",
        "Time (sec)",
    )

    preprocessing_time = []
    query_times = []
    for ratio in ratios:
        print("=================", "ratio:", ratio, "=================")
        path = (
            "real_data/"
            + datasets[idx]
            + "/"
            + datasets[idx]
            + "_r_"
            + str(ratio)
            + ".csv"
        )
        num_of_buckets = 100
        disparity, distribution, ranking, theta, duration = find_fair_ranking(
            path, columns[idx], sensitive_attrs[idx], num_of_buckets
        )
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

    print("Varying minority ratio (prep time):", preprocessing_time)
    print("Varying minority ratio (query time):", query_times)
    plot(
        "plots/ranking_2d/" + datasets[idx] + "/varying_ratio_prep_time.png",
        ratios,
        preprocessing_time,
        ratios,
        "Varying ratio (prep time)",
        "Ratio",
        "Time (sec)",
    )
    plot(
        "plots/ranking_2d/" + datasets[idx] + "/varying_ratio_query_time.png",
        ratios,
        query_times,
        ratios,
        "Varying ratio (query time)",
        "Ratio",
        "Time (sec)",
    )

    preprocessing_time = []
    query_times = []
    for num_of_buckets in num_of_buckets_list:
        print(
            "=================",
            "number of buckets:",
            num_of_buckets,
            "=================",
        )
        path = "real_data/" + datasets[idx] + "/" + datasets[idx] + "_r_0.25.csv"
        disparity, distribution, ranking, theta, duration = find_fair_ranking(
            path, columns[idx], sensitive_attrs[idx], num_of_buckets
        )
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

    print("Varying number of buckets (prep time):", preprocessing_time)
    print("Varying number of buckets (query time):", query_times)
    plot(
        "plots/ranking_2d/" + datasets[idx] + "/varying_num_of_buckets_prep_time.png",
        num_of_buckets_list,
        preprocessing_time,
        num_of_buckets_list,
        "Varying number of buckets (prep time)",
        "Number of buckets",
        "Time (sec)",
    )
    plot(
        "plots/ranking_2d/" + datasets[idx] + "/varying_num_of_buckets_query_time.png",
        num_of_buckets_list,
        query_times,
        num_of_buckets_list,
        "Varying number of buckets (query time)",
        "Number of buckets",
        "Time (sec)",
    )
