from collections import Counter

import numpy as np
import pandas as pd
from scipy.special import comb

from ranking_util import basestuff, TwoD
from utils import rank
from copy import deepcopy

def ranking_sampled(path, sample, columns, number_of_buckets, sens_attr):
    n = sample.shape[0]
    basestuff.read_df(sample, columns)
    dataset = pd.read_csv(path)
    dataset = dataset[[col for col in columns]]
    dataset["idx"] = [float(i) for i in range(dataset.shape[0])]
    dataset = dataset.to_numpy()
    
    R = []
    Theta = []
    TwoD.initialize()
    for i in range(n * n):
        r_, _, theta = TwoD.GetNext()
        r = deepcopy(r_)
        if r is not None:
            projection = rank(dataset, [theta], len(columns))
            R.append(projection)
            Theta.append(theta)
        else:
            break
    F = find_fair_ranking(path, R, sens_attr, number_of_buckets)
    # print("Fairness:", F[0], F[1], R[F[2]])
    return Theta[F[3]], F[0],F[1]


def find_fair_ranking(path, R, sens_attr_col, number_of_buckets):
    df = pd.read_csv(path)
    sens_attr_values = np.unique(df[sens_attr_col])
    freq = Counter(list(pd.read_csv(path)[sens_attr_col].values))
    minority = min(freq, key=freq.get)
    distributions = []
    collision_prob = {}
    for r in R:
        print(R.index(r),"of",len(R))
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


def generate_sample(path, frac):
    return pd.read_csv(path).sample(frac=frac)

