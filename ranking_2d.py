import timeit

import numpy as np
import pandas as pd
from scipy.special import comb
from ranking_util import basestuff, TwoD


def get_all_rankings(path, columns):
    n = pd.read_csv(path).shape[0]
    basestuff.read_file(file=path, columns=columns)
    R = []
    for i in range(n * n):
        r, _ = TwoD.GetNext()
        if r is None:
            break
        R.append(r)
    return R


def find_fair_ranking(path, columns, sens_attr_col, number_of_buckets):
    G = list(pd.read_csv(path)[sens_attr_col].values)
    n = len(G)
    start = timeit.default_timer()
    R = get_all_rankings(path, columns=columns)
    stop = timeit.default_timer()
    sens_attr_values = np.unique(G)
    distributions = []
    collision_prob = {}
    bucket_size = n // number_of_buckets

    for r in R:
        bucket_distribution = []
        collision_count = {}

        for j in range(number_of_buckets):
            bucket = []
            for k in range(bucket_size):
                bucket.append(G[r[j * bucket_size + k]])
            bucket_distribution.append([bucket.count(sens_attr) / bucket_size for sens_attr in sens_attr_values])
            for sens_attr in sens_attr_values:
                if sens_attr in collision_count.keys():
                    collision_count[sens_attr] += comb(bucket.count(sens_attr), len(sens_attr_values))
                else:
                    collision_count[sens_attr] = comb(bucket.count(sens_attr), len(sens_attr_values))

        for sens_attr in sens_attr_values:
            if sens_attr in collision_prob.keys():
                collision_prob[sens_attr].append(
                    collision_count[sens_attr] / comb(G.count(sens_attr), len(sens_attr_values)))
            else:
                collision_prob[sens_attr] = [
                    collision_count[sens_attr] / comb(G.count(sens_attr), len(sens_attr_values))]

        distributions.append(bucket_distribution)

    disparity = []
    for i in range(len(collision_prob[sens_attr])):
        max_collision_prob = np.max([collision_prob[sens_attr][i] for sens_attr in sens_attr_values])
        min_collision_prob = np.min([collision_prob[sens_attr][i] for sens_attr in sens_attr_values])
        disparity.append((max_collision_prob / min_collision_prob) - 1)

    return min(disparity), distributions[disparity.index(min(disparity))], R[
        disparity.index(min(disparity))], stop - start


# TODO: add query function to 2D ranking
def query(q):
    return
