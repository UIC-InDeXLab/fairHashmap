import timeit
from bisect import bisect
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from scipy.special import comb
from ranking_util import basestuff, TwoD
from copy import deepcopy


def get_all_rankings(path, columns, G, number_of_buckets):
    if isinstance(path, pd.DataFrame):
        n = path.shape[0]
        basestuff.read_df(dataframe=path, columns=columns)
    else:
        n = pd.read_csv(path).shape[0]
        basestuff.read_file(file=path, columns=columns)

    bucket_size = n // number_of_buckets
    TwoD.initialize()
    R = []
    Theta = []
    boundary_indices = [k * bucket_size for k in range(1, number_of_buckets)]
    swap_index = []
    count = 0
    for i in range(n * n):
        r_, j, theta = TwoD.GetNext()
        r = deepcopy(r_)
        count += 1
        if r is not None and j != -1:
            if i == 0 or (j + 1 in boundary_indices and G[r[j]] != G[r[j + 1]]):
                # print("r", j, j+1, r[j], r[j+1], [r[idx * bucket_size:(
                #     idx+1) * bucket_size] for idx in range(number_of_buckets)])
                # print()

                R.append(r)
                Theta.append(theta)
                swap_index.append(j)
        elif r is not None and j == -1:
            R.append(r)
            Theta.append(theta)
            swap_index.append(j)
        else:
            break
    print(count, len(R))
    print()
    return R, Theta, swap_index


def find_fair_ranking(path, columns, sens_attr_col, number_of_buckets):
    if isinstance(path, pd.DataFrame):
        G = list(path[sens_attr_col].values)
    else:
        G = list(pd.read_csv(path)[sens_attr_col].values)
    freq = Counter(G)
    minority = min(freq, key=freq.get)
    n = len(G)
    bucket_size = n // number_of_buckets
    start = timeit.default_timer()
    R, Theta, swap_index = get_all_rankings(path, columns, G, number_of_buckets)

    sens_attr_values = {val: idx for idx, val in enumerate(np.unique(G).tolist())}
    collision_prob = defaultdict(list)

    first = R[0]
    bucket_distribution = [
        [0 for _ in range(len(sens_attr_values.keys()))]
        for _ in range(number_of_buckets)
    ]

    collision_count = defaultdict(int)

    for i in range(number_of_buckets):
        bucket = []
        for j in range(bucket_size):
            bucket.append(G[first[i * bucket_size + j]])
        for key, val in sens_attr_values.items():
            bucket_distribution[i][val] = bucket.count(key)
            collision_count[key] += comb(bucket_distribution[i][val], 2)
    for key in sens_attr_values.keys():
        collision_prob[key].append(collision_count[key] / comb(G.count(key), 2))

    # print("first", [first[i * bucket_size:(i+1) * bucket_size]
    #       for i in range(number_of_buckets)])
    # print(bucket_distribution)
    print(len(first))
    for i in range(1, len(R)):
        j = swap_index[i]
        g_left = G[R[i][j + 1]]
        g_right = G[R[i][j]]
        bucket_left = j // bucket_size
        bucket_right = bucket_left + 1
        # print("R", j, j+1, R[i][j], R[i][j+1], [R[i][idx * bucket_size:(idx+1) * bucket_size]
        #       for idx in range(number_of_buckets)])
        # print(g_left, g_right, bucket_left, bucket_right)
        # print(bucket_distribution[bucket_left])
        # print(bucket_distribution[bucket_right])
        # print()

        collision_count[g_right] -= comb(
            bucket_distribution[bucket_left][sens_attr_values[g_right]], 2
        )
        collision_count[g_left] -= comb(
            bucket_distribution[bucket_left][sens_attr_values[g_left]], 2
        )
        collision_count[g_right] -= comb(
            bucket_distribution[bucket_right][sens_attr_values[g_right]], 2
        )
        collision_count[g_left] -= comb(
            bucket_distribution[bucket_right][sens_attr_values[g_left]], 2
        )

        bucket_distribution[bucket_left][sens_attr_values[g_right]] += 1
        bucket_distribution[bucket_left][sens_attr_values[g_left]] -= 1
        bucket_distribution[bucket_right][sens_attr_values[g_right]] -= 1
        bucket_distribution[bucket_right][sens_attr_values[g_left]] += 1

        collision_count[g_right] += comb(
            bucket_distribution[bucket_left][sens_attr_values[g_right]], 2
        )
        collision_count[g_left] += comb(
            bucket_distribution[bucket_left][sens_attr_values[g_left]], 2
        )
        collision_count[g_right] += comb(
            bucket_distribution[bucket_right][sens_attr_values[g_right]], 2
        )
        collision_count[g_left] += comb(
            bucket_distribution[bucket_right][sens_attr_values[g_left]], 2
        )

        for key in sens_attr_values.keys():
            collision_prob[key].append(collision_count[key] / comb(G.count(key), 2))

    disparity = []
    for i in range(len(collision_prob[minority])):
        max_collision_prob = np.max(
            [collision_prob[sens_attr][i] for sens_attr in sens_attr_values]
        )
        min_collision_prob = np.min(
            [collision_prob[sens_attr][i] for sens_attr in sens_attr_values]
        )
        disparity.append((max_collision_prob / min_collision_prob) - 1)

    stop = timeit.default_timer()

    max_collision_prob_original = np.max(
        [collision_prob[sens_attr][0] for sens_attr in sens_attr_values]
    )
    min_collision_prob_original = np.min(
        [collision_prob[sens_attr][0] for sens_attr in sens_attr_values]
    )
    print(max_collision_prob_original,min_collision_prob_original)
    disparity_original = (max_collision_prob_original / min_collision_prob_original) - 1

    return (
        min(disparity),
        disparity_original,
        R[disparity.index(min(disparity))],
        Theta[disparity.index(min(disparity))],
        stop - start,
    )


def query(q, f, scores, d, number_of_buckets):
    c = 0
    for j in range(d):
        c += f[j] * q[j]
    hash_bucket = (bisect(scores, c) // (len(scores) // number_of_buckets)) + 1
    return hash_bucket
