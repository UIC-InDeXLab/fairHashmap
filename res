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
    female_collision_prob = []
    male_collision_prob = []

    bucket_size = n // number_of_buckets
    minority_count = G.count(sens_attr_values[0])
    for r in R:
        ratios = []
        collision_count={}
        female_collision_count = 0
        male_collision_count = 0

        for j in range(number_of_buckets):
            bucket = []
            for k in range(bucket_size):
                bucket.append(G[r[j * bucket_size + k]])
            ratios.append([bucket.count(sens_attr) / bucket_size for sens_attr in sens_attr_values])
            for sens_attr in sens_attr_values:
                collision_count

            female_collision_count += comb(bucket.count(sens_attr_values[0]), 2)
            male_collision_count += comb(bucket.count(sens_attr_values[1]), 2)

        female_collision_prob.append(female_collision_count / comb(minority_count, 2))
        male_collision_prob.append(male_collision_count / comb(n - minority_count, 2))
        all_possible_ratios.append(ratios)

    div_disparity = []
    sub_disparity = []
    for i in range(len(female_collision_prob)):
        if male_collision_prob[i] > female_collision_prob[i]:
            div_disparity.append((male_collision_prob[i] / female_collision_prob[i]) - 1)
        else:
            div_disparity.append((female_collision_prob[i] / male_collision_prob[i]) - 1)
        sub_disparity.append(abs(male_collision_prob[i] - female_collision_prob[i]))

    # print('Division based disparity for all rankings:', div_disparity)
    # print('Minimum division based disparity:', min(div_disparity), ", index:", div_disparity.index(min(div_disparity)))
    # print('Subtraction based disparity for all rankings:', sub_disparity)
    # print('Minimum subtraction based disparity:', min(sub_disparity), ", index:",
    #       sub_disparity.index(min(sub_disparity)))
    # print(all_possible_ratios[div_disparity.index(min(div_disparity))])
    # print(R[div_disparity.index(min(div_disparity))])
    print(div_disparity)
    return R, all_possible_ratios, div_disparity, R[div_disparity.index(min(div_disparity))]


# ---------------------------------------------------------------------------------------------------------------------
ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
sizes = [1000]
num_of_buckets = [10, 100, 1000, 10000, 100000]

durations = []
for size in sizes:
    rankings, _, _, _, duration = find_fair_ranking("data/2d_sample_0.1_" + str(size) + ".csv", "S", ["F", "M"], 100)
    durations.append(duration)
print("Varying dataset size:", durations)

durations = []
for ratio in ratios:
    rankings, _, _, _, duration = find_fair_ranking("data/2d_sample_" + str(ratio) + "_1000000.csv", "S", ["F", "M"],
                                                    100)
    durations.append(duration)
print("Varying minority ratio:", durations)

durations = []
for num_of_bucket in num_of_buckets:
    rankings, _, _, _, duration = find_fair_ranking("data/2d_sample_0.1_1000000.csv", "S", ["F", "M"], num_of_bucket)
    durations.append(duration)
print("Varying bucket size:", durations)
