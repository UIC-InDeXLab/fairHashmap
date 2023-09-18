import timeit
import numpy as np
from sweep_and_cut import sweep_and_cut, query
from utils import plot, plot_3
from pathlib import Path

queries = []
for i in range(1000):
    query_x = np.random.randint(0, 100000)
    query_y = np.random.randint(0, 100000)
    queries.append([query_x, query_y])

ratios = [0.25, 0.5, 0.75, 1.0]
g1 = [4000, 6666, 8000, 10000]
g2 = [16000, 13334, 12000, 10000]
fractions = [0.2, 0.4, 0.6, 0.8, 1.0]
num_of_buckets_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
datasets = ["adult", "compas"]
sensitive_attrs = ["sex", "Sex_Code_Text"]
columns = [["fnlwgt", "education-num"], ["Person_ID", "Case_ID"]]

for idx in range(len(datasets)):
    print("=================", datasets[idx], "=================")
    preprocessing_time = []
    space = []
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
        boundary, hash_buckets, duration = sweep_and_cut(
            path, columns[idx], sensitive_attrs[idx], num_of_buckets
        )
        preprocessing_time.append(duration)
        space.append(len(boundary))
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q[0], boundary, hash_buckets)
            stop = timeit.default_timer()
            query_time.append(stop - start)
        query_times.append(np.mean(query_time))
    print("Varying dataset size (prep time):", preprocessing_time)
    print("Varying dataset size (query time):", query_times)
    print("Varying dataset size (space):", space)
    Path("plots/sweep_and_cut/" +
         datasets[idx]).mkdir(parents=True, exist_ok=True)
    plot(
        "plots/sweep_and_cut/" + datasets[idx] + "/varying_size_prep_time.png",
        fractions,
        preprocessing_time,
        fractions,
        "Varying dataset size (prep time)",
        "Fraction",
        "Time (sec)",
    )
    plot(
        "plots/sweep_and_cut/" +
        datasets[idx] + "/varying_size_query_time.png",
        fractions,
        query_times,
        fractions,
        "Varying dataset size (query time)",
        "Fraction",
        "Time (sec)",
    )

    plot(
        "plots/sweep_and_cut/" + datasets[idx] + "/varying_size_space.png",
        fractions,
        space,
        fractions,
        "Varying dataset size (space)",
        "Fraction",
        "Number of cuts",
    )

    preprocessing_time = []
    space = []
    upperbound = []
    query_times = []
    for idx2, ratio in enumerate(ratios):
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
        boundary, hash_buckets, duration = sweep_and_cut(
            path, columns[idx], sensitive_attrs[idx], num_of_buckets
        )
        preprocessing_time.append(duration)
        space.append(len(boundary))
        ub = 2*((g1[idx2]*g2[idx2]/20000)+100)
        upperbound.append(ub)
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q[0], boundary, hash_buckets)
            stop = timeit.default_timer()
            query_time.append(stop - start)
        query_times.append(np.mean(query_time))
    print("Varying minority ratio (prep time):", preprocessing_time)
    print("Varying minority ratio (query time):", query_times)
    print("Varying minority ratio (space):", space)
    plot(
        "plots/sweep_and_cut/" +
        datasets[idx] + "/varying_ratio_prep_time.png",
        ratios,
        preprocessing_time,
        ratios,
        "Varying ratio (prep time)",
        "Ratio",
        "Time (sec)",
    )
    plot(
        "plots/sweep_and_cut/" +
        datasets[idx] + "/varying_ratio_query_time.png",
        ratios,
        query_times,
        ratios,
        "Varying ratio (query time)",
        "Ratio",
        "Time (sec)",
    )
    plot(
        "plots/sweep_and_cut/" + datasets[idx] + "/varying_ratio_space.png",
        ratios,
        space,
        ratios,
        "Varying ratio (space)",
        "Ratio",
        "Number of cuts",
    )

    plot_3(
        "plots/sweep_and_cut/" + datasets[idx] + "/varying_ratio_space_.png",
        ratios,
        space,
        upperbound,
        ratios,
        "Varying ratio (space)",
        "Ratio",
        "Number of cuts",
    )

    preprocessing_time = []
    space = []
    query_times = []
    for num_of_buckets in num_of_buckets_list:
        print(
            "=================",
            "number of buckets:",
            num_of_buckets,
            "=================",
        )
        path = "real_data/" + datasets[idx] + \
            "/" + datasets[idx] + "_r_0.25.csv"
        boundary, hash_buckets, duration = sweep_and_cut(
            path, columns[idx], sensitive_attrs[idx], num_of_buckets
        )
        preprocessing_time.append(duration)
        space.append(len(boundary))
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q[0], boundary, hash_buckets)
            stop = timeit.default_timer()
            query_time.append(stop - start)
        query_times.append(np.mean(query_time))
    print("Varying bucket size (prep time):", preprocessing_time)
    print("Varying bucket size (query time):", query_times)
    print("Varying bucket size (space):", space)
    plot(
        "plots/sweep_and_cut/"
        + datasets[idx]
        + "/varying_num_of_buckets_prep_time.png",
        num_of_buckets_list,
        preprocessing_time,
        num_of_buckets_list,
        "Varying number of buckets (prep time)",
        "Number of buckets",
        "Time (sec)",
    )
    plot(
        "plots/sweep_and_cut/"
        + datasets[idx]
        + "/varying_num_of_buckets_query_time.png",
        num_of_buckets_list,
        query_times,
        num_of_buckets_list,
        "Varying number of buckets (query time)",
        "Number of buckets",
        "Time (sec)",
    )
    plot(
        "plots/sweep_and_cut/" + datasets[idx] +
        "/varying_num_of_buckets_space.png",
        num_of_buckets_list,
        space,
        num_of_buckets_list,
        "Varying number of buckets (space)",
        "Number of buckets",
        "Number of cuts",
    )
print(
    "###############################################################################################################"
)
