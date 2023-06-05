import numpy as np
import pandas as pd
from scipy.special import comb
from ranking import basestuff, TwoD


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


def find_fair_ranking(path, columns, sens_attr, number_of_buckets):
    G = list(pd.read_csv(path)[sens_attr].values)
    n = len(G)
    R = get_all_rankings(path, columns=columns)
    sens_attr_values = np.unique(G)
    all_possible_ratios = []
    collision_prob = {}
    bucket_size = n // number_of_buckets

    for r in R:
        ratios = []
        collision_count = {}

        for j in range(number_of_buckets):
            bucket = []
            for k in range(bucket_size):
                bucket.append(G[r[j * bucket_size + k]])
            ratios.append([bucket.count(sens_attr) / bucket_size for sens_attr in sens_attr_values])
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
        all_possible_ratios.append(ratios)

    disparity = []

    for sens_attr in sens_attr_values:
        for i in range(len(collision_prob[sens_attr])):
            average_collision_prob = np.mean([collision_prob[sens_attr_][i] for sens_attr_ in sens_attr_values])
            if collision_prob[sens_attr][i] < average_collision_prob:
                disparity.append((average_collision_prob / collision_prob[sens_attr][i]) - 1)
            else:
                disparity.append((collision_prob[sens_attr][i] / average_collision_prob) - 1)
        # print('Division based disparity for all rankings:', disparity)
        print('Minimum division based disparity:', min(disparity), ", index:", disparity.index(min(disparity)))
        print(all_possible_ratios[disparity.index(min(disparity))])
        print(R[disparity.index(min(disparity))])
    # return R, all_possible_ratios, disparity, R[disparity.index(min(disparity))]


# ---------------------------------------------------------------------------------------------------------------------
# ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
# sizes = [1000]
# num_of_buckets = [10, 100, 1000, 10000, 100000]

find_fair_ranking("data/2d_sample_0.2_1000.csv", ["X1", "X2"], "S", 10)

# durations = []
# for size in sizes:
#     rankings, _, _, _, duration = find_fair_ranking("data/2d_sample_0.1_" + str(size) + ".csv", "S", ["F", "M"], 100)
#     durations.append(duration)
# print("Varying dataset size:", durations)
#
# durations = []
# for ratio in ratios:
#     rankings, _, _, _, duration = find_fair_ranking("data/2d_sample_" + str(ratio) + "_1000000.csv", "S", ["F", "M"],
#                                                     100)
#     durations.append(duration)
# print("Varying minority ratio:", durations)
#
# durations = []
# for num_of_bucket in num_of_buckets:
#     rankings, _, _, _, duration = find_fair_ranking("data/2d_sample_0.1_1000000.csv", "S", ["F", "M"], num_of_bucket)
#     durations.append(duration)
# print("Varying bucket size:", durations)
