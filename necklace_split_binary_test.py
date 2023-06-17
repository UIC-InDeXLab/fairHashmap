import timeit
import numpy as np
from necklace_split_binary import necklace_split, query

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

for idx in range(len(datasets)):
    print("=================", datasets[idx], "=================")
    preprocessing_time = []
    space = []
    query_times = []
    for frac in fractions:
        print("=================", "fraction:", frac, "=================")
        path = "real_data/" + datasets[idx] + "/" + datasets[idx] + "_f_" + str(frac) + ".csv"
        num_of_buckets = 100
        _, boundary, hash_buckets, duration = necklace_split(path, columns[idx],
                                                             sensitive_attrs[idx], num_of_buckets)
        preprocessing_time.append(duration)
        space.append(len(boundary))
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q[0], boundary, hash_buckets)
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
        print("=================", "ratio:", ratio, "=================")
        path = "real_data/" + datasets[idx] + "/" + datasets[idx] + "_r_" + str(ratio) + ".csv"
        num_of_buckets = 100
        _, boundary, hash_buckets, duration = necklace_split(path, columns[idx],
                                                             sensitive_attrs[idx], num_of_buckets)
        preprocessing_time.append(duration)
        space.append(len(boundary))
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q[0], boundary, hash_buckets)
            stop = timeit.default_timer()
            query_time.append(stop - start)
        query_times.append(np.mean(query_time))
    print("Varying minority ratio:", preprocessing_time)
    print("Varying minority ratio (query time):", query_times)
    print("Varying minority ratio (space):", space)

    preprocessing_time = []
    space = []
    query_times = []
    for num_of_buckets in num_of_buckets_list:
        print("=================", "number of buckets:", num_of_buckets, "=================")
        path = "real_data/" + datasets[idx] + "/" + datasets[idx] + "_r_0.25.csv"
        _, boundary, hash_buckets, duration = necklace_split(path, columns[idx],
                                                             sensitive_attrs[idx], num_of_buckets)
        preprocessing_time.append(duration)
        space.append(len(boundary))
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q[0], boundary, hash_buckets)
            stop = timeit.default_timer()
            query_time.append(stop - start)
        query_times.append(np.mean(query_time))
    print("Varying bucket size:", preprocessing_time)
    print("Varying bucket size (query time):", query_times)
    print("Varying bucket size (space):", space)
    print("########################################################################################################")
