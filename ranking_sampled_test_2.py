import timeit

import numpy as np

from ranking_2d import find_fair_ranking, query
from utils import read_df, score, polartoscalar, plot, plot_2
from pathlib import Path
from ranking_sampled import generate_sample


queries = []
for i in range(1000):
    query_x = np.random.randint(0, 100000)
    query_y = np.random.randint(0, 100000)
    queries.append([query_x, query_y])

ratios = [0.25, 0.5, 0.75, 1.0]
fractions = [0.2, 0.4, 0.6, 0.8, 1.0]
num_of_buckets_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
datasets = [
    "adult",
    "compas",
]
sensitive_attrs = [
    "sex",
    "Sex_Code_Text",
]
columns = [
    ["fnlwgt", "education-num"],
    ["Person_ID", "Case_ID"],
]
d = 2
flag = 0
for idx in range(len(datasets)):
    print("=================", datasets[idx], "=================")
    preprocessing_time = []
    query_times = []
    disparities_after = []
    disparities_before = []
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
        sample = generate_sample(path, 0.1)
        num_of_buckets = 100
        (
            disparity,
            disparity_original,
            distribution,
            ranking,
            theta,
            duration,
        ) = find_fair_ranking(sample, columns[idx], sensitive_attrs[idx], num_of_buckets)
        print("Disparity:", disparity)
        print("Original Disparity:", disparity_original)
        disparities_after.append(disparity)
        disparities_before.append(disparity_original)
        preprocessing_time.append(duration)
        query_time = []
        dataset = read_df(sample, columns[idx])
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
    
    Path("plots/ranking_sampled_2/" + datasets[idx]).mkdir(parents=True, exist_ok=True)
    
    plot_2(
        "plots/ranking_sampled_2/" + datasets[idx] + "/varying_size_unfairness.png",
        fractions,
        disparities_before,
        disparities_after,
        fractions,
        "Varying dataset size (Disparity Before/After)",
        "Fraction",
        "Disparity Before/After",
    )

    plot(
        "plots/ranking_sampled_2/" + datasets[idx] + "/varying_size_prep_time.png",
        fractions,
        preprocessing_time,
        fractions,
        "Varying dataset size (prep time)",
        "Fraction",
        "Time (sec)",
    )
    plot(
        "plots/ranking_sampled_2/" + datasets[idx] + "/varying_size_query_time.png",
        fractions,
        query_times,
        fractions,
        "Varying dataset size (query time)",
        "Fraction",
        "Time (sec)",
        [5e-7,15e-7]
    )

    preprocessing_time = []
    query_times = []
    disparities_after = []
    disparities_before = []
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
        sample = generate_sample(path, 0.1)
        num_of_buckets = 100
        (
            disparity,
            disparity_original,
            distribution,
            ranking,
            theta,
            duration,
        ) = find_fair_ranking(sample, columns[idx], sensitive_attrs[idx], num_of_buckets)
        print("Disparity:", disparity)
        print("Original Disparity:", disparity_original)
        preprocessing_time.append(duration)
        disparities_after.append(disparity)
        disparities_before.append(disparity_original)

        dataset = read_df(sample, columns[idx])
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
    plot_2(
        "plots/ranking_sampled_2/" + datasets[idx] + "/varying_ratio_unfairness.png",
        ratios,
        disparities_before,
        disparities_after,
        ratios,
        "Varying ratio (Disparity Before/After)",
        "Ratio",
        "Disparity Before/After",
    )
    plot(
        "plots/ranking_sampled_2/" + datasets[idx] + "/varying_ratio_prep_time.png",
        ratios,
        preprocessing_time,
        ratios,
        "Varying ratio (prep time)",
        "Ratio",
        "Time (sec)",
    )
    plot(
        "plots/ranking_sampled_2/" + datasets[idx] + "/varying_ratio_query_time.png",
        ratios,
        query_times,
        ratios,
        "Varying ratio (query time)",
        "Ratio",
        "Time (sec)",
        [5e-7,15e-7]
    )

    preprocessing_time = []
    query_times = []
    disparities_after = []
    disparities_before = []
    for num_of_buckets in num_of_buckets_list:
        print(
            "=================",
            "number of buckets:",
            num_of_buckets,
            "=================",
        )
        path = "real_data/" + datasets[idx] + "/" + datasets[idx] + "_r_0.25.csv"
        sample = generate_sample(path, 0.1)
        (
            disparity,
            disparity_original,
            distribution,
            ranking,
            theta,
            duration,
        ) = find_fair_ranking(sample, columns[idx], sensitive_attrs[idx], num_of_buckets)
        print("Disparity:", disparity)
        print("Original Disparity:", disparity_original)
        preprocessing_time.append(duration)
        disparities_after.append(disparity)
        disparities_before.append(disparity_original)

        dataset = read_df(sample, columns[idx])
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

    plot_2(
        "plots/ranking_sampled_2/" + datasets[idx] + "/varying_num_of_buckets_unfairness.png",
        num_of_buckets_list,
        disparities_before,
        disparities_after,
        num_of_buckets_list,
        "Varying number of buckets (Disparity Before/After)",
        "Number of buckets",
        "Disparity Before/After",
    )
    plot(
        "plots/ranking_sampled_2/" + datasets[idx] + "/varying_num_of_buckets_prep_time.png",
        num_of_buckets_list,
        preprocessing_time,
        num_of_buckets_list,
        "Varying number of buckets (prep time)",
        "Number of buckets",
        "Time (sec)",
    )
    plot(
        "plots/ranking_sampled_2/" + datasets[idx] + "/varying_num_of_buckets_query_time.png",
        num_of_buckets_list,
        query_times,
        num_of_buckets_list,
        "Varying number of buckets (query time)",
        "Number of buckets",
        "Time (sec)",
        [5e-7,15e-7]
    )