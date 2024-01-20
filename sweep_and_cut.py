import timeit

import numpy as np
import pandas as pd
from collections import defaultdict, Counter
from bisect import bisect


def sweep_and_cut(path, column, sens_attr, num_of_buckets):
    df = pd.read_csv(path)
    start = timeit.default_timer()
    df = df.sort_values(column[0])
    t = df[column[0]].values
    G = df[sens_attr].values
    G_unique, G_count = np.unique(df[sens_attr].values, return_counts=True)
    n = df.shape[0]
    C = np.zeros(len(G_unique), dtype=int)
    w = np.zeros(n, dtype=int)
    for i in range(n):
        g = np.where(G_unique == G[i])[0][0]
        w[i] = (C[g] // (G_count[g] / num_of_buckets)) + 1
        C[g] += 1
    hash_buckets = []
    boundary = []
    i = 0
    while True:
        while i < n - 1 and w[i] == w[i + 1]:
            i += 1
        if i == n - 1:
            break
        hash_buckets.append(w[i])
        boundary.append((t[i] + t[i + 1]) / 2)
        if i == n - 2:
            hash_buckets.append(w[i])
            boundary.append(t[i])
            break
        i += 1
    stop = timeit.default_timer()
    return boundary, hash_buckets, stop - start


def query(q, boundary, hash_buckets):
    idx = bisect(boundary, q)
    if idx == len(hash_buckets):
        return hash_buckets[-1]
    else:
        return hash_buckets[idx]

def fit_predict_eval_sweep(path_train, path_test, column,sens_attr_col,num_of_buckets):
    boundary, hash_buckets,_=sweep_and_cut(path_test,column,sens_attr_col,num_of_buckets)
    test=pd.read_csv(path_train)
    dict=defaultdict(list)
    G = list(test[sens_attr_col].values)
    n = len(G)
    freq = Counter(G)
    sens_attr_values = np.unique(G)
    
    for _, row in test.iterrows():
        bucket = query(row[column[0]], boundary, hash_buckets)
        dict[bucket].append(row[sens_attr_col])         
        
    collision_prob_single = defaultdict(int)
    collision_prob_pairwise = defaultdict(int)
    collision_prob=0
    
    for bucket in dict.values():
        collision_prob += (len(bucket)/n)**2 
        for val in sens_attr_values:
            collision_prob_single[val] += (bucket.count(val)/freq[val])*(len(bucket)/n)
            collision_prob_pairwise[val] += (bucket.count(val)/freq[val])**2
    
    max_collision_prob_single = np.max(
        [collision_prob_single[sens_attr] for sens_attr in sens_attr_values]
    )
    min_collision_prob_single = np.min(
        [collision_prob_single[sens_attr] for sens_attr in sens_attr_values]
    )
    single_fairness= (max_collision_prob_single / (min_collision_prob_single)) - 1
            
    max_collision_prob_pairwise = np.max(
        [collision_prob_pairwise[sens_attr] for sens_attr in sens_attr_values]
    )
    min_collision_prob_pairwise = np.min(
        [collision_prob_pairwise[sens_attr] for sens_attr in sens_attr_values]
    )
    
    pairwise_fairness= (max_collision_prob_pairwise / (min_collision_prob_pairwise)) - 1
    
    return collision_prob, single_fairness, pairwise_fairness
    # return collision_prob, collision_prob_single, collision_prob_pairwise