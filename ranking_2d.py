import timeit
from bisect import bisect
from collections import Counter

import numpy as np
import pandas as pd
from scipy.special import comb

from ranking_util import basestuff, TwoD


def get_all_rankings(path, columns, G, number_of_buckets):
    n = pd.read_csv(path).shape[0]
    bucket_size = n // number_of_buckets
    basestuff.read_file(file=path, columns=columns)
    TwoD.initialize()
    R = []
    Theta = []
    boundary_indices = []
    for i in range(n * n):
        r, j, theta = TwoD.GetNext()
        if r is not None and j != -1:
            idx1 = r[j]
            idx2 = r[j + 1]
            if i == 0 or (idx2 in boundary_indices and G[idx1] != G[idx2]):
                boundary_indices = [
                    r[k * bucket_size] for k in range(number_of_buckets)
                ]
                R.append(r)
                Theta.append(theta)

        elif r is not None and j == -1:
            boundary_indices = [r[k * bucket_size] for k in range(number_of_buckets)]
            R.append(r)
            Theta.append(theta)
        else:
            break

    return R, Theta


def find_fair_ranking(path, columns, sens_attr_col, number_of_buckets):
    G = list(pd.read_csv(path)[sens_attr_col].values)
    freq = Counter(G)
    minority = min(freq, key=freq.get)
    n = len(G)
    bucket_size = n // number_of_buckets
    start = timeit.default_timer()
    R, Theta = get_all_rankings(path, columns, G, number_of_buckets)
    sens_attr_values = np.unique(G)
    distributions = []
    collision_prob = {}

    for idx in range(len(R)):
        bucket_distribution = []
        collision_count = {}

        for j in range(number_of_buckets):
            bucket = []
            for k in range(bucket_size):
                bucket.append(G[R[idx][j * bucket_size + k]])
            bucket_distribution.append(
                [
                    bucket.count(sens_attr) / bucket_size
                    for sens_attr in sens_attr_values
                ]
            )
            for val in sens_attr_values:
                if val in collision_count.keys():
                    collision_count[val] += comb(bucket.count(val), 2)
                else:
                    collision_count[val] = comb(bucket.count(val), 2)

        for val in sens_attr_values:
            if val in collision_prob.keys():
                collision_prob[val].append(collision_count[val] / comb(G.count(val), 2))
            else:
                collision_prob[val] = [collision_count[val] / comb(G.count(val), 2)]

        distributions.append(bucket_distribution)

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
    return (
        min(disparity),
        distributions[disparity.index(min(disparity))],
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
