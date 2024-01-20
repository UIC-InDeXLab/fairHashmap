import timeit

import numpy as np
import pandas as pd

from ranking_sampled_vector import find_fair_ranking, query
from utils import read_file, score, polartoscalar, plot, plot_2
from pathlib import Path
from necklace_split_binary import necklace_split
import pickle


queries = []
for i in range(1000):
    query_x = np.random.randint(0, 1)
    query_y = np.random.randint(0, 1)
    queries.append([query_x, query_y])

ratios = [0.25, 0.5, 0.75, 1.0]
n_vectors=[10,50,100,500,1000]
# n_vectors=[1000,1000,1000,1000,1000]

fractions = [0.2, 0.4, 0.6, 0.8, 1.0]
num_of_buckets_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
datasets = ["adult", "compas_random_id", "diabetes", "popsim_binary"]
sensitive_attrs = ["sex", "Sex_Code_Text", "gender", "race"]
columns = [
    ["fnlwgt", "education-num"],
    ["ID", "RawScore"],
    ["encounter_id", "patient_nbr"],
    ["lon", "lat"],
]
d = 2
for idx in range(len(datasets)):
    preprocessing_time_t = []
    query_times_t = []
    disparities_after_t = []
    disparities_before_t = []
    print("=================", datasets[idx], "=================")
    for i in range(5):
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
            n = pd.read_csv(path).shape[0]
            num_of_buckets = 100
            (
                disparity,
                disparity_original,
                ranking,
                theta,
                duration,
            ) = find_fair_ranking(path, n_vectors[idx], columns[idx], sensitive_attrs[idx], num_of_buckets)
            # print("Disparity:", disparity)
            # print("Original Disparity:", disparity_original)
            disparities_after.append(disparity)
            disparities_before.append(disparity_original)
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
    print("Disparity Before:",disparities_before)
    print("Disparity After:",disparities_after)


    Path("plots/ranking_sampled_vector/" + datasets[idx]).mkdir(parents=True, exist_ok=True)

    plot_2(
        "plots/ranking_sampled_vector/" + datasets[idx] + "/varying_size_unfairness.png",
        fractions,
        disparities_before,
        disparities_after,
        fractions,
        "Varying dataset size (Disparity Before/After)",
        "Fraction(×"+str(n)+")",
        "Disparity Before/After",
    )

    plot(
        "plots/ranking_sampled_vector/" + datasets[idx] + "/varying_size_prep_time.png",
        fractions,
        preprocessing_time,
        fractions,
        "Varying dataset size (prep time)",
        "Fraction(×"+str(n)+")",
        "Time (sec)",
    )
    plot(
        "plots/ranking_sampled_vector/" + datasets[idx] + "/varying_size_query_time.png",
        fractions,
        query_times,
        fractions,
        "Varying dataset size (query time)",
        "Fraction(×"+str(n)+")",
        "Time (sec)",
        [5e-7, 15e-7],
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
            + "_2/"
            + datasets[idx]
            + "_r_"
            + str(ratio)
            + ".csv"
        )
        num_of_buckets = 100
        (
            disparity,
            disparity_original,
            ranking,
            theta,
            duration,
        ) = find_fair_ranking(path, n_vectors[idx], columns[idx], sensitive_attrs[idx], num_of_buckets)
        # print("Disparity:", disparity)
        # print("Original Disparity:", disparity_original)
        preprocessing_time.append(duration)
        disparities_after.append(disparity)
        disparities_before.append(disparity_original)

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
        
        preprocessing_time_t.append(preprocessing_time)
        query_times_t.append(query_times)
        disparities_after_t.append(disparities_after)
        disparities_before_t.append(disparities_before)

    print("Varying number of vectors (prep time):", np.mean(preprocessing_time_t,axis=0))
    print("Varying number of vectors (query time):", np.mean(query_times_t,axis=0))
    print("Disparity Before:",np.mean(disparities_before_t,axis=0))
    print("Disparity After:",np.mean(disparities_after_t,axis=0))

    print("Varying minority ratio (prep time):", preprocessing_time)
    print("Varying minority ratio (query time):", query_times)
    print("Disparity Before:",disparities_before)
    print("Disparity After:",disparities_after)
    plot_2(
        "plots/ranking_sampled_vector/" + datasets[idx] + "/varying_ratio_unfairness.png",
        ratios,
        disparities_before,
        disparities_after,
        ratios,
        "Varying ratio (Disparity Before/After)",
        "Ratio",
        "Disparity Before/After",
    )
    plot(
        "plots/ranking_sampled_vector/" + datasets[idx] + "/varying_ratio_prep_time.png",
        ratios,
        preprocessing_time,
        ratios,
        "Varying ratio (prep time)",
        "Ratio",
        "Time (sec)",
    )
    plot(
        "plots/ranking_sampled_vector/" + datasets[idx] + "/varying_ratio_query_time.png",
        ratios,
        query_times,
        ratios,
        "Varying ratio (query time)",
        "Ratio",
        "Time (sec)",
        [5e-7, 15e-7],
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
        (
            disparity,
            disparity_original,
            ranking,
            theta,
            duration,
        ) = find_fair_ranking(path, n_vectors[idx], columns[idx], sensitive_attrs[idx], num_of_buckets)
        print("Disparity:", disparity)
        print("Original Disparity:", disparity_original)
        preprocessing_time.append(duration)
        disparities_after.append(disparity)
        disparities_before.append(disparity_original)

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
    print("Disparity Before:",disparities_before)
    print("Disparity After:",disparities_after)

    plot_2(
        "plots/ranking_sampled_vector/" + datasets[idx] + "/varying_num_of_buckets_unfairness.png",
        num_of_buckets_list,
        disparities_before,
        disparities_after,
        num_of_buckets_list,
        "Varying number of buckets (Disparity Before/After)",
        "Number of buckets",
        "Disparity Before/After",
    )
    plot(
        "plots/ranking_sampled_vector/" + datasets[idx] + "/varying_num_of_buckets_prep_time.png",
        num_of_buckets_list,
        preprocessing_time,
        num_of_buckets_list,
        "Varying number of buckets (prep time)",
        "Number of buckets",
        "Time (sec)",
    )
    plot(
        "plots/ranking_sampled_vector/" + datasets[idx] + "/varying_num_of_buckets_query_time.png",
        num_of_buckets_list,
        query_times,
        num_of_buckets_list,
        "Varying number of buckets (query time)",
        "Number of buckets",
        "Time (sec)",
        [5e-7, 15e-7],
    )
    
    # preprocessing_time_t = []
    # query_times_t = []
    # disparities_after_t = []
    # disparities_before_t = []
    # for n_vector in n_vectors:
    #     preprocessing_time = []
    #     query_times = []
    #     disparities_after = []
    #     disparities_before = []
    #     for i in range(1):      
    #         print("=================", "n_vector:", n_vector, "=================")
    #         path = (
    #             "real_data/"
    #             + datasets[idx]
    #             + "/"
    #             + datasets[idx]
    #             + "_f_0.2.csv"
    #         )
    #         n = pd.read_csv(path).shape[0]
    #         sex=pd.read_csv(path)[sensitive_attrs[idx]].to_list()
    #         num_of_buckets = 100
    #         (
    #             disparity,
    #             disparity_original,
    #             ranking,
    #             theta,
    #             duration,
    #         ) = find_fair_ranking(path, n_vector, columns[idx], sensitive_attrs[idx], num_of_buckets)
            
    #         out=[0 if sex[val]=="P1_003N" else 1 for val in ranking]
    #         with open('ordering_'+datasets[idx]+'.pkl', 'wb') as f:
    #             pickle.dump(out, f)
    #         disparities_after.append(disparity)
    #         disparities_before.append(disparity_original)
    #         preprocessing_time.append(duration)
    #         query_time = []
    #         dataset = read_file(path, columns[idx])
    #         f = polartoscalar([theta], d)
    #         scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])
    #         for q in queries:
    #             start = timeit.default_timer()
    #             query(q, f, scores, d, num_of_buckets)
    #             stop = timeit.default_timer()
    #             query_time.append(stop - start)
    #         query_times.append(np.mean(query_time))
    #     preprocessing_time_t.append(preprocessing_time)
    #     query_times_t.append(query_times)
    #     disparities_after_t.append(disparities_after)
    #     disparities_before_t.append(disparities_before)

    # print("Varying number of vectors (prep time):", np.mean(preprocessing_time_t,axis=1))
    # print("Varying number of vectors (query time):", np.mean(query_times_t,axis=1))
    # print("Disparity Before:",np.mean(disparities_before_t,axis=1))
    # print("Disparity After:",np.mean(disparities_after_t,axis=1))
        
print(
    "###############################################################################################################"
)