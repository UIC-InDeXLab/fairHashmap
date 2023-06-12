import math
from collections import Counter

import numpy as np
import pandas as pd
from scipy.special import comb

from necklace_split_binary import necklace_split
from ranking_util import basestuff, TwoD
from utils import rank


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
            bucket_distribution.append([bucket.count(sens_attr) / bucket_size for sens_attr in sens_attr_values])
            for val in sens_attr_values:
                if val in collision_count.keys():
                    collision_count[val] += comb(bucket.count(val), len(sens_attr_values))
                else:
                    collision_count[val] = comb(bucket.count(val), len(sens_attr_values))
        for val in sens_attr_values:
            if val in collision_prob.keys():
                collision_prob[val].append(
                    collision_count[val] / comb(G.count(val), len(sens_attr_values)))
            else:
                collision_prob[val] = [
                    collision_count[val] / comb(G.count(val), len(sens_attr_values))]
        distributions.append(bucket_distribution)

    disparity = []
    for i in range(len(collision_prob[minority])):
        max_collision_prob = np.max([collision_prob[val][i] for val in sens_attr_values])
        min_collision_prob = np.min([collision_prob[val][i] for val in sens_attr_values])
        disparity.append((max_collision_prob / min_collision_prob) - 1)

    return min(disparity), distributions[disparity.index(min(disparity))], disparity.index(min(disparity))


def hybrid_with_sampling(path, sample, columns, number_of_buckets, sens_attr):
    n = sample.shape[0]
    basestuff.read_df(sample, columns)

    dataset = pd.read_csv(path)
    dataset = dataset[[col for col in columns]]
    dataset["idx"] = [float(i) for i in range(dataset.shape[0])]
    dataset = dataset.to_numpy()
    R_1 = []
    R_2 = []
    Theta = []
    number_of_cuts = []
    for i in range(n * n):
        r, _, theta = TwoD.GetNext()  # vector and boundary based on sample
        if r is None:
            break
        projection = rank(dataset, [theta], len(columns))  # vector based on sample boundary based on original input
        R_1.append(r)
        R_2.append(projection)
        Theta.append(theta)
        _, boundary, _, _ = necklace_split(path, columns[0], sens_attr, number_of_buckets, projection)
        number_of_cuts.append(len(boundary))

    F_1 = find_fair_ranking(path, R_1, sens_attr, number_of_buckets)
    F_2 = find_fair_ranking(path, R_2, sens_attr, number_of_buckets)
    print("Vector and boundary based on sample:", F_1[0], F_1[1], R_1[F_1[2]])
    print("Vector based on sample, boundary based on original input:", F_2[0], F_2[1], R_2[F_1[2]])
    print("Min number of cuts after necklace splitting:", np.min(number_of_cuts))
    return Theta[F_1[2]], Theta[F_2[2]]


def generate_sample(path, number_of_dimensions, number_of_buckets, sens_attr):
    df = pd.read_csv(path)
    sens_attr_values = np.unique(list(df[sens_attr].values))
    n = df.shape[0]
    merge = []
    for val in sens_attr_values:
        merge.append(df[df[sens_attr] == val].sample(
            int(np.ceil(12 * number_of_buckets * number_of_dimensions * math.log(n) / 50))))
    return pd.concat(merge, axis=0).sample(frac=1.0).reset_index()
