import math
import timeit

import numpy as np
import pandas as pd
from ranking_util import basestuff, TwoD
from necklace_split_binary import necklace_split
from scipy.special import comb


def find_fair_ranking(path, R, sens_attr_col, number_of_buckets):
    df = pd.read_csv(path)
    start = timeit.default_timer()
    stop = timeit.default_timer()
    distributions = []
    collision_prob = {}
    for r in R:
        G = [list(df[sens_attr_col].values)[i] for i in r]
        sens_attr_values = np.unique(G)
        bucket_size = len(r) // number_of_buckets
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


def score(dataset, i, f, d):
    c = 0
    if len(f) != d:
        print('Error: Function length should be equal to d')
        return
    for j in range(d):
        c += f[j] * dataset[i, j]
    return c


def rank(dataset, theta, d):
    f = polartoscalar(theta, d)
    r = sorted([[i, score(dataset, i, f, d)] for i in range(len(dataset))], key=lambda x: x[1], reverse=True)
    return tuple([r[i][0] for i in range(len(r))])


def polartoscalar(theta, d, r=1):
    f = []
    for j in range(d - 1, 0, -1):
        f.insert(0, r * math.sin(theta[j - 1]))
        r *= math.cos(theta[j - 1])
    f.insert(0, r)
    return f


def hybrid_with_sampling(path, sample, columns, number_of_buckets, sens_attr):
    n = sample.shape[0]
    basestuff.read_df(sample, columns)

    dataset = pd.read_csv(path)
    dataset = dataset[[col for col in columns]]
    dataset["idx"] = [float(i) for i in range(dataset.shape[0])]
    dataset = dataset.to_numpy()
    R_1 = []
    R_2 = []
    number_of_cuts = []
    for i in range(n * n):
        r, _, theta = TwoD.GetNext()  # vector and boundary based on sample
        if r is None:
            break
        projection = rank(dataset, [theta], len(columns))  # vector based on sample boundary based on original input
        R_1.append(r)
        R_2.append(projection)
        _, boundary, _, _ = necklace_split(path, columns[0], sens_attr, number_of_buckets, projection)
        number_of_cuts.append(len(boundary))
    print("Vector and boundary based on sample:")
    print(find_fair_ranking(path, R_1, sens_attr, number_of_buckets))
    print("Vector based on sample, boundary based on original input:")
    print(find_fair_ranking(path, R_2, sens_attr, number_of_buckets))
    print("Min number of cuts after necklace splitting:")
    print(np.min(number_of_cuts))

def generate_sample(path, number_of_dimensions, number_of_buckets, sens_attr):
    df = pd.read_csv(path)
    sens_attr_values = np.unique(list(df[sens_attr].values))
    n = df.shape[0]
    merge = []
    for val in sens_attr_values:
        merge.append(df[df[sens_attr] == val].sample(
            int(np.ceil(12 * number_of_buckets * number_of_dimensions * math.log(n) / 50))))
    return pd.concat(merge, axis=0).sample(frac=1.0).reset_index()
