import itertools
import timeit
from bisect import bisect
import numpy as np
import pandas as pd


def necklace_split(path, col, sens_attr, sens_attr_values, num_of_buckets):
    df = pd.read_csv(path).sample(frac=1.0)
    start = timeit.default_timer()
    # df = df.sort_values(col)
    size = df.shape[0]
    G = list(df[sens_attr].values)
    T = list(df[col].values)
    c_F_total = G.count(sens_attr_values[0])
    c_M_total = G.count(sens_attr_values[1])
    n = len(G)
    indices = [i for i in range(n)]
    arc_size = int(np.ceil((c_F_total + c_M_total) / num_of_buckets))
    hash_buckets = []
    boundary = []
    offset = 0
    for j in range(num_of_buckets):
        if offset + arc_size <= n:
            c_F_ = G[offset: arc_size + offset].count(sens_attr_values[0])
            c_M_ = G[offset: arc_size + offset].count(sens_attr_values[1])
        else:
            if offset <= n:
                c_F_ = list(itertools.chain(G[offset:n], G[:(offset + arc_size) % n])).count(sens_attr_values[0])
                c_M_ = list(itertools.chain(G[offset:n], G[:(offset + arc_size) % n])).count(sens_attr_values[1])
            else:
                if offset % n <= (offset + arc_size) % n:
                    c_F_ = G[offset % n:(offset + arc_size) % n].count(sens_attr_values[0])
                    c_M_ = G[offset % n:(offset + arc_size) % n].count(sens_attr_values[1])
                else:
                    c_F_ = list(itertools.chain(G[offset % n:n], G[:(offset + arc_size) % n])).count(
                        sens_attr_values[0])
                    c_M_ = list(itertools.chain(G[offset % n:n], G[:(offset + arc_size) % n])).count(
                        sens_attr_values[1])

        print('starting counts:', c_F_, c_M_)
        print('G', G)
        print('indices', indices)
        for i in range(n):
            if i + offset != offset:
                if i + offset + arc_size <= n:
                    if G[i + offset - 1] == sens_attr_values[0] and G[i + offset + arc_size - 1] == sens_attr_values[1]:
                        c_F_ -= 1
                        c_M_ += 1
                    if G[i + offset - 1] == sens_attr_values[1] and G[i + offset + arc_size - 1] == sens_attr_values[0]:
                        c_F_ += 1
                        c_M_ -= 1
                    print(c_F_, c_M_, G[i + offset:i + offset + arc_size], indices[i + offset:i + offset + arc_size])
                else:
                    if i + offset <= n:
                        if G[i + offset - 1] == sens_attr_values[0] and G[(i + offset + arc_size) % n - 1] == \
                                sens_attr_values[1]:
                            c_F_ -= 1
                            c_M_ += 1
                        if G[i + offset - 1] == sens_attr_values[1] and G[(i + offset + arc_size) % n - 1] == \
                                sens_attr_values[0]:
                            c_F_ += 1
                            c_M_ -= 1
                        print(c_F_, c_M_, list(itertools.chain(G[i + offset:n], G[:(i + offset + arc_size) % n])),
                              indices[i + offset:n] + indices[:(i + offset + arc_size) % n])
                    else:
                        if (i + offset) % n <= (i + offset + arc_size) % n:

                            if G[(i + offset) % n - 1] == sens_attr_values[0] and G[(i + offset + arc_size) % n - 1] == \
                                    sens_attr_values[1]:
                                c_F_ -= 1
                                c_M_ += 1
                            if G[(i + offset) % n - 1] == sens_attr_values[1] and G[(i + offset + arc_size) % n - 1] == \
                                    sens_attr_values[0]:
                                c_F_ += 1
                                c_M_ -= 1
                            print(c_F_, c_M_, G[(i + offset) % n:(i + offset + arc_size) % n],
                                  indices[(i + offset) % n:(i + offset + arc_size) % n])

                        else:
                            if G[(i + offset + arc_size) % n - 1] == sens_attr_values[1] and G[(i + offset) % n - 1] == \
                                    sens_attr_values[0]:
                                c_F_ += 1
                                c_M_ -= 1
                            if G[(i + offset + arc_size) % n - 1] == sens_attr_values[0] and G[(i + offset) % n - 1] == \
                                    sens_attr_values[1]:
                                c_F_ -= 1
                                c_M_ += 1
                            print(c_F_, c_M_,
                                  list(itertools.chain(G[(i + offset) % n:n], G[:(i + offset + arc_size) % n])),
                                  indices[(i + offset) % n:n] + indices[:(i + offset + arc_size) % n])

            if c_F_ == int(np.ceil(c_F_total / num_of_buckets)) and c_M_ == int(np.ceil(c_M_total / num_of_buckets)):
                break
        if i + offset + arc_size < n:
            if i + offset != 0 and i + offset != size:
                boundary.append(indices[i + offset])
                boundary.append(indices[i + offset + arc_size])
                hash_buckets.extend([j, j])
            if i + offset == offset:
                print(c_F_, c_M_, G[i + offset: i + offset + arc_size], indices[i + offset: i + offset + arc_size])
            del G[i + offset: i + offset + arc_size]
            del indices[i + offset: i + offset + arc_size]
            if n != 0:
                offset = (offset + i) % n
        else:
            if i + offset < n:
                if i + offset != 0 and i + offset != size:
                    boundary.append(indices[i + offset])
                    boundary.append(indices[(i + offset + arc_size) % n])
                    hash_buckets.extend([j, j])
                if i + offset == offset:
                    print(c_F_, c_M_, G[i + offset: n] + G[:(i + offset + arc_size) % n],
                          indices[i + offset: n] + indices[:(i + offset + arc_size) % n])
                del G[i + offset: n], G[:(i + offset + arc_size) % n]
                del indices[i + offset: n], indices[:(i + offset + arc_size) % n]
                offset = 0
            else:
                if (i + offset) % n < (i + offset + arc_size) % n:
                    if (i + offset) % n != 0 and (i + offset) % n != size:
                        boundary.append(indices[(i + offset) % n])
                        boundary.append(indices[(i + offset + arc_size) % n])
                        hash_buckets.extend([j, j])
                    if i + offset == offset:
                        print(c_F_, c_M_, G[(i + offset) % n:(i + offset + arc_size) % n],
                              indices[(i + offset) % n:(i + offset + arc_size) % n])
                    del G[(i + offset) % n:(i + offset + arc_size) % n]
                    del indices[(i + offset) % n:(i + offset + arc_size) % n]
                    offset = (i + offset) % n
                else:
                    if (i + offset) % n != 0 and (i + offset) % n != size:
                        boundary.append(indices[(i + offset) % n])
                        boundary.append(indices[(i + offset + arc_size) % n])
                        hash_buckets.extend([j, j])
                    if i + offset == offset:
                        print(c_F_, c_M_, G[(i + offset) % n:n], G[:(i + offset + arc_size) % n],
                              indices[(i + offset) % n:n] + indices[:(i + offset + arc_size) % n])
                    del G[(i + offset) % n:n], G[:(i + offset + arc_size) % n]
                    del indices[(i + offset) % n:n], indices[:(i + offset + arc_size) % n]
                    offset = (i + offset) % n
        n = n - arc_size
        print('offset', offset)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    stop = timeit.default_timer()
    return stop - start, \
        [T[val] for val in np.unique(sorted(boundary), return_index=True)[0]], \
        [hash_buckets[idx] for idx in np.unique(sorted(boundary), return_index=True)[1]]


def query(q, boundary, hash_buckets):
    return hash_buckets[bisect(boundary, q)]


duration, boundary, hash_buckets = necklace_split("data/2d_sample_0.2_10000.csv", "X1", "S", ["F", "M"], 50)
print(len(boundary))

# -----------------------------------------Experiments-----------------------------------------------------
# ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
# sizes = [1000, 10000, 100000, 1000000, 10000000]
# num_of_buckets = [10, 100, 1000, 10000, 100000]
# queries = list(np.random.uniform(0, 1, 100))
#
# preprocessing_time = []
# space = []
# query_times = []
# for size in sizes:
#     duration, boundary, hash_buckets_ = necklace_split("data/2d_sample_0.1_" + str(size) + ".csv", "X1", "S",
#                                                        ["F", "M"], 100)
#     preprocessing_time.append(duration)
#     space.append(len(boundary))
#     query_time = []
#     for q in queries:
#         start = timeit.default_timer()
#         query(q, boundary, hash_buckets_)
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
#     duration, boundary, hash_buckets_ = necklace_split("data/2d_sample_" + str(ratio) + "_1000000.csv", "X1",
#                                                        "S", ["F", "M"], 100)
#     preprocessing_time.append(duration)
#     space.append(len(boundary))
#     query_time = []
#     for q in queries:
#         start = timeit.default_timer()
#         query(q, boundary, hash_buckets_)
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
#     duration, boundary, hash_buckets_ = necklace_split("data/2d_sample_0.1_1000000.csv", "X1", "S", ["F", "M"],
#                                                        num_of_bucket)
#     preprocessing_time.append(duration)
#     space.append(len(boundary))
#     query_time = []
#     for q in queries:
#         start = timeit.default_timer()
#         query(q, boundary, hash_buckets_)
#         stop = timeit.default_timer()
#         query_time.append(stop - start)
#     query_times.append(np.mean(query_time))
# print("Varying bucket size:", preprocessing_time)
# print("Varying bucket size (query time):", query_times)
# print("Varying bucket size (space):", space)
