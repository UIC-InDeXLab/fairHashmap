import itertools
import timeit

import numpy as np
import pandas as pd


def necklace_split(path, ranking, col, sens_attr, sens_attr_values, num_of_buckets):
    df = pd.read_csv(path)
    start = timeit.default_timer()
    G = [list(df[sens_attr].values)[i] for i in ranking]
    T = [list(df[col].values)[i] for i in ranking]
    size = df.shape[0]
    c_F_total = G.count(sens_attr_values[0])
    c_M_total = G.count(sens_attr_values[1])
    n = len(G)
    indices = [i for i in range(n)]
    arc_size = int(np.ceil((c_F_total + c_M_total) / num_of_buckets))
    hash_buckets = []
    boundary = []
    offset = 0
    ordering = []
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

        # print('starting counts:', c_F_, c_M_)
        # print('G', G)
        # print('indices', indices)
        for i in range(n):
            if i + offset != offset:
                if i + offset + arc_size <= n:
                    if G[i + offset - 1] == sens_attr_values[0] and G[i + offset + arc_size - 1] == sens_attr_values[1]:
                        c_F_ -= 1
                        c_M_ += 1
                    if G[i + offset - 1] == sens_attr_values[1] and G[i + offset + arc_size - 1] == sens_attr_values[0]:
                        c_F_ += 1
                        c_M_ -= 1
                    # print(c_F_, c_M_, G[i + offset:i + offset + arc_size], indices[i + offset:i + offset + arc_size])
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
                        # print(c_F_, c_M_, list(itertools.chain(G[i + offset:n], G[:(i + offset + arc_size) % n])),
                        #       indices[i + offset:n] + indices[:(i + offset + arc_size) % n])
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
                            # print(c_F_, c_M_, G[(i + offset) % n:(i + offset + arc_size) % n],
                            #       indices[(i + offset) % n:(i + offset + arc_size) % n])

                        else:
                            if G[(i + offset + arc_size) % n - 1] == sens_attr_values[1] and G[(i + offset) % n - 1] == \
                                    sens_attr_values[0]:
                                c_F_ += 1
                                c_M_ -= 1
                            if G[(i + offset + arc_size) % n - 1] == sens_attr_values[0] and G[(i + offset) % n - 1] == \
                                    sens_attr_values[1]:
                                c_F_ -= 1
                                c_M_ += 1
                            # print(c_F_, c_M_,
                            #       list(itertools.chain(G[(i + offset) % n:n], G[:(i + offset + arc_size) % n])),
                            #       indices[(i + offset) % n:n] + indices[:(i + offset + arc_size) % n])

            if c_F_ == int(np.ceil(c_F_total / num_of_buckets)) and c_M_ == int(np.ceil(c_M_total / num_of_buckets)):
                break
        if i + offset + arc_size < n:
            if i + offset != 0 and i + offset != size:
                boundary.append(indices[i + offset])
                boundary.append(indices[i + offset + arc_size])
                hash_buckets.extend([j, j])
            # if i + offset == offset:
            #     print(c_F_, c_M_, G[i + offset: i + offset + arc_size], indices[i + offset: i + offset + arc_size])
            ordering.append(G[i + offset: i + offset + arc_size])
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
                # if i + offset == offset:
                #     print(c_F_, c_M_, G[i + offset: n] + G[:(i + offset + arc_size) % n],
                #           indices[i + offset: n] + indices[:(i + offset + arc_size) % n])
                ordering.append(G[i + offset: n] + G[:(i + offset + arc_size) % n])
                del G[i + offset: n], G[:(i + offset + arc_size) % n]
                del indices[i + offset: n], indices[:(i + offset + arc_size) % n]

                offset = 0
            else:
                if (i + offset) % n < (i + offset + arc_size) % n:
                    if (i + offset) % n != 0 and (i + offset) % n != size:
                        boundary.append(indices[(i + offset) % n])
                        boundary.append(indices[(i + offset + arc_size) % n])
                        hash_buckets.extend([j, j])
                    # if i + offset == offset:
                    #     print(c_F_, c_M_, G[(i + offset) % n:(i + offset + arc_size) % n],
                    #           indices[(i + offset) % n:(i + offset + arc_size) % n])
                    ordering.append(G[(i + offset) % n:(i + offset + arc_size) % n])
                    del G[(i + offset) % n:(i + offset + arc_size) % n]
                    del indices[(i + offset) % n:(i + offset + arc_size) % n]
                    offset = (i + offset) % n
                else:
                    if (i + offset) % n != 0 and (i + offset) % n != size:
                        boundary.append(indices[(i + offset) % n])
                        boundary.append(indices[(i + offset + arc_size) % n])
                        hash_buckets.extend([j, j])
                    # if i + offset == offset:
                    #     print(c_F_, c_M_, G[(i + offset) % n:n], G[:(i + offset + arc_size) % n],
                    #           indices[(i + offset) % n:n] + indices[:(i + offset + arc_size) % n])
                    ordering.append(G[(i + offset) % n:n] + G[:(i + offset + arc_size) % n])
                    del G[(i + offset) % n:n], G[:(i + offset + arc_size) % n]
                    del indices[(i + offset) % n:n], indices[:(i + offset + arc_size) % n]
                    offset = (i + offset) % n
        n = n - arc_size
        # print('offset', offset)
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    stop = timeit.default_timer()
    return stop - start, \
        [T[val] for val in np.unique(sorted(boundary), return_index=True)[0]], \
        [hash_buckets[idx] for idx in np.unique(sorted(boundary), return_index=True)[1]], \
        ordering, np.unique(sorted(boundary))

# path = "data/2d_sample_0.2_100.csv"
# number_of_buckets = 10
# rankings, all_possible_ratios, _, fair_ranking, _ = find_fair_ranking(path, "S", ["F", "M"], number_of_buckets)
# number_of_cuts = []
# orderings = []
# for i in range(len(rankings)):
#     # print(i, "of", len(rankings))
#     _, boundary, _, ordering = necklace_split(path, rankings[i], "X1", "S", ["F", "M"], number_of_buckets)
#     number_of_cuts.append(len(boundary))
#     orderings.append(ordering)
#
# df = pd.read_csv(path)
# n = df.shape[0]
# bucket_length = n // number_of_buckets
# sorted_list_of_cuts = sorted(number_of_cuts)
# sorted_list_of_cuts_indices = np.argsort(number_of_cuts)
#
# for idx in range(20):
#     print("number of cuts:", sorted_list_of_cuts[idx], "index:", sorted_list_of_cuts_indices[idx])
#     G = [list(df["S"].values)[i] for i in rankings[sorted_list_of_cuts_indices[idx]]]
#     print("Original ranking:", [G[bucket_length * i:bucket_length * (i + 1)] for i in range(number_of_buckets)])
#     print("Original ranking counts:", [[G[bucket_length * i:bucket_length * (i + 1)].count('F'),
#                                         G[bucket_length * i:bucket_length * (i + 1)].count('M')] for i in
#                                        range(number_of_buckets)])
#     print("Ordering after necklace:", orderings[sorted_list_of_cuts_indices[idx]])
#     print("Ordering after necklace counts:",
#           [[bucket.count('F'), bucket.count('M')] for bucket in orderings[sorted_list_of_cuts_indices[idx]]])
#     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#
# print("=========================================================================")
# G = [list(df["S"].values)[i] for i in fair_ranking]
#
# _, boundary, _, ordering = necklace_split(path, fair_ranking, "X1", "S", ["F", "M"], number_of_buckets)
# print("Fairest ranking after necklace:", ordering)
# print("Fairest ranking after necklace counts:",
#       [[bucket.count('F'), bucket.count('M')] for bucket in ordering])
# print("number of cuts:", len(boundary))
#
# print("Original fairest ranking:", [G[bucket_length * i:bucket_length * (i + 1)] for i in range(number_of_buckets)])
# print("Original fairest ranking counts:", [[G[bucket_length * i:bucket_length * (i + 1)].count('F'),
#                                             G[bucket_length * i:bucket_length * (i + 1)].count('M')] for i in
#                                            range(number_of_buckets)])

# At this point, not sure about the ranking code.
