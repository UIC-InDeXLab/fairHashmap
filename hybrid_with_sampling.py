import math
import timeit
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from scipy.special import comb

from necklace_split_binary import necklace_split
from ranking_util import basestuff, TwoD
from utils import rank
from copy import deepcopy


def find_fair_ranking(path, R, sens_attr_col, number_of_buckets):
    df = pd.read_csv(path)
    sens_attr_values = np.unique(df[sens_attr_col])
    freq = Counter(list(pd.read_csv(path)[sens_attr_col].values))
    minority = min(freq, key=freq.get)
    distributions = []
    collision_prob = {}
    for r in R:
        G = [list(df[sens_attr_col].values)[i] for i in r]
        bucket_size = len(r) // number_of_buckets
        bucket_distribution = []
        collision_count = {}
        for j in range(number_of_buckets):
            bucket = []
            for k in range(bucket_size):
                bucket.append(G[r[j * bucket_size + k]])
            bucket_distribution.append(
                [
                    bucket.count(sens_attr) / bucket_size
                    for sens_attr in sens_attr_values
                ]
            )
            for val in sens_attr_values:
                if val in collision_count.keys():
                    collision_count[val] += comb(
                        bucket.count(val), len(sens_attr_values)
                    )
                else:
                    collision_count[val] = comb(
                        bucket.count(val), len(sens_attr_values)
                    )
        for val in sens_attr_values:
            if val in collision_prob.keys():
                collision_prob[val].append(
                    collision_count[val] / comb(G.count(val), len(sens_attr_values))
                )
            else:
                collision_prob[val] = [
                    collision_count[val] / comb(G.count(val), len(sens_attr_values))
                ]
        distributions.append(bucket_distribution)

    disparity = []
    for i in range(len(collision_prob[minority])):
        max_collision_prob = np.max(
            [collision_prob[val][i] for val in sens_attr_values]
        )
        min_collision_prob = np.min(
            [collision_prob[val][i] for val in sens_attr_values]
        )
        disparity.append((max_collision_prob / min_collision_prob) - 1)

    max_collision_prob_original = np.max(
        [collision_prob[sens_attr][0] for sens_attr in sens_attr_values]
    )
    min_collision_prob_original = np.min(
        [collision_prob[sens_attr][0] for sens_attr in sens_attr_values]
    )
    disparity_original = (max_collision_prob_original / min_collision_prob_original) - 1
    
    return (
        min(disparity),
        disparity_original,
        distributions[disparity.index(min(disparity))],
        disparity.index(min(disparity)),
    )


# flag=0: vector and boundary based on sample, flag=1: vector based on sample boundary based on original input
def hybrid_with_sampling(path, sample, columns, number_of_buckets, sens_attr, flag):
    n = sample.shape[0]
    basestuff.read_df(sample, columns)
    G = list(sample[sens_attr].values)
    dataset = pd.read_csv(path)
    dataset = dataset[[col for col in columns]]
    dataset["idx"] = [float(i) for i in range(dataset.shape[0])]
    dataset = dataset.to_numpy()
    bucket_size = n // number_of_buckets
    R = []
    Theta = []
    number_of_cuts = []
    TwoD.initialize()
    for i in range(n * n):
        r_, j, theta = TwoD.GetNext()
        r = deepcopy(r_)
        if r is not None and j != -1:
            boundary_indices = [r[k * bucket_size] for k in range(number_of_buckets)]
            idx1 = r[j]
            idx2 = r[j + 1]
            if i == 0 or (idx2 in boundary_indices and G[idx1] != G[idx2]):
                if not flag:
                    R.append(r)
                else:
                    projection = rank(dataset, [theta], len(columns))
                    R.append(projection)
                    # _, boundary, _, _ = necklace_split(path, columns[0], sens_attr, number_of_buckets, projection, theta)
                    # number_of_cuts.append(len(boundary))
        elif r is not None and j == -1:
            boundary_indices = [r[k * bucket_size] for k in range(number_of_buckets)]
            if not flag:
                R.append(r)
            else:
                projection = rank(dataset, [theta], len(columns))
                R.append(projection)
                # _, boundary, _, _ = necklace_split(path, columns[0], sens_attr, number_of_buckets, projection, theta)
                # number_of_cuts.append(len(boundary))
        else:
            break
        Theta.append(theta)
    F = find_fair_ranking(path, R, sens_attr, number_of_buckets)
    # print("Fairness:", F[0], F[1], R[F[2]])
    # if flag:
    # print("Min number of cuts after necklace splitting:", np.min(number_of_cuts))

    return Theta[F[3]], F[0],F[1]


def generate_sample(path, d, number_of_buckets, sens_attr):
    df = pd.read_csv(path)
    sens_attr_values = np.unique(list(df[sens_attr].values))
    n = df.shape[0]
    merge = []
    for val in sens_attr_values:
        sample_size = int(np.ceil(12 * number_of_buckets * d * math.log(n) / 50))
        merge.append(df[df[sens_attr] == val].sample(sample_size))
    return pd.concat(merge, axis=0).sample(frac=1.0).reset_index()


def generate_sample(path, frac):
    return pd.read_csv(path).sample(frac=frac)

