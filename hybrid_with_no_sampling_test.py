import timeit

import numpy as np
from hybrid_with_no_sampling import hybrid_with_no_sampling
from necklace_split_binary import query

queries = []
for i in range(100):
    query_x = np.random.uniform(0, 500000)
    query_y = np.random.uniform(0, 16)
    queries.append([query_x, query_y])

ratios = [0.25, 0.5, 0.75, 1.0]
fractions = [0.2, 0.4, 0.6, 0.9, 1.0]
num_of_buckets = [100, 200, 300, 400, 500, 600, 700, 800, 1000]
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
        num_of_cuts, boundary, hash_buckets, theta, duration = hybrid_with_no_sampling(path, sensitive_attrs[idx],
                                                                                       columns[idx], num_of_buckets)
        preprocessing_time.append(duration)
        space.append(len(boundary))
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q, boundary, hash_buckets, [theta])
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
        num_of_cuts, boundary, hash_buckets, theta, duration = hybrid_with_no_sampling(path, sensitive_attrs[idx],
                                                                                       columns[idx], num_of_buckets)
        preprocessing_time.append(duration)
        space.append(len(boundary))
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q, boundary, hash_buckets, [theta])
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
        print("=================", "number of buckets:", num_of_bucket, "=================")
        path = "real_data/" + datasets[idx] + "/" + datasets[idx] + "_r_1.0.csv"
        num_of_cuts, boundary, hash_buckets, theta, duration = hybrid_with_no_sampling(path, sensitive_attrs[idx],
                                                                                       columns[idx], num_of_buckets)
        preprocessing_time.append(duration)
        space.append(len(boundary))
        query_time = []
        for q in queries:
            start = timeit.default_timer()
            query(q, boundary, hash_buckets, [theta])
            stop = timeit.default_timer()
            query_time.append(stop - start)
        query_times.append(np.mean(query_time))
    print("Varying bucket size:", preprocessing_time)
    print("Varying bucket size (query time):", query_times)
    print("Varying bucket size (space):", space)
print("###############################################################################################################")

# path = "synthetic_data/2d_sample_0.2_100.csv"
# number_of_buckets = 10
# num_of_cuts, boundary, hash_buckets, theta = hybrid_with_no_sampling(path, "S", ["X1", "X2"], number_of_buckets)
# print(queries[0])
# print(boundary)
# print(hash_buckets)
# print(query(queries[0], boundary, hash_buckets, [theta]))
