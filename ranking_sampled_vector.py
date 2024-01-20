import math
import numpy as np
import pandas as pd
from utils import rank, read_file, score, polartoscalar
from collections import Counter, defaultdict
# from scipy.special import comb
import timeit
from bisect import bisect
from copy import deepcopy


def ranking_sampled_vector(path, n_vectors, columns):
    Theta=list(np.random.uniform(low=0,high=math.pi / 2, size=n_vectors))
    Theta.insert(0,0)
    dataset=read_file(path,columns)
    R=[]
    for theta in Theta:
        r=deepcopy(rank(dataset,[theta],2))
        R.append(r)
    return R, Theta


def find_fair_ranking(path, n_vectors, columns, sens_attr_col, number_of_buckets):
    start = timeit.default_timer()
    R,Theta = ranking_sampled_vector(path, n_vectors, columns)
    df = pd.read_csv(path)
    G_=list(df[sens_attr_col].values)
    G = [G_[i] for i in R[0]] 
    sens_attr_values = np.unique(df[sens_attr_col])
    freq = Counter(G)
    minority = min(freq, key=freq.get)
    # distributions = []
    collision_prob_dict = defaultdict(list)
    for r in R:
        bucket_size = len(r) // number_of_buckets
        bucket_distribution = []
        # collision_count = defaultdict(int)
        for j in range(number_of_buckets):
            bucket = []
            for k in range(bucket_size):
                bucket.append(G[r[j * bucket_size + k]])
            bucket_distribution.append(bucket)
            # bucket_distribution.append(
            #     [
            #         bucket.count(sens_attr)/bucket_size
            #         for sens_attr in sens_attr_values
            #     ]
            # )
            # for val in sens_attr_values:
            #     collision_count[val] += comb(
            #             bucket.count(val), len(sens_attr_values)
            #         )
            # print(bucket)
            
        for val in sens_attr_values:  
            collision_prob=0  
            for bucket in bucket_distribution:
                # collision_prob_dict[val].append(
                #     collision_count[val] / comb(G.count(val), len(sens_attr_values))
                # )
                collision_prob+= (bucket.count(val)/freq[val])**2
            collision_prob_dict[val].append(collision_prob)
        # distributions.append(bucket_distribution)
    disparity = []
    for i in range(len(collision_prob_dict[minority])):
        max_collision_prob_dict = np.max(
            [collision_prob_dict[val][i] for val in sens_attr_values]
        )
        min_collision_prob_dict = np.min(
            [collision_prob_dict[val][i] for val in sens_attr_values]
        )
        disparity.append((max_collision_prob_dict / min_collision_prob_dict) - 1)

    stop = timeit.default_timer()
    max_collision_prob_dict_original = np.max(
        [collision_prob_dict[sens_attr][0] for sens_attr in sens_attr_values]
    )
    min_collision_prob_dict_original = np.min(
        [collision_prob_dict[sens_attr][0] for sens_attr in sens_attr_values]
    )
    disparity_original = (max_collision_prob_dict_original / min_collision_prob_dict_original) - 1

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


def fit_predict_eval(path_train, path_test,n_vectors, column,sens_attr_col,num_of_buckets):
    _, _, _, theta, _ = find_fair_ranking(path_train, n_vectors, column, sens_attr_col, num_of_buckets)
    dataset = read_file(path_train, column)
    f = polartoscalar([theta], 2)
    scores = sorted([score(dataset[i], f, 2) for i in range(len(dataset))])
    
    test=pd.read_csv(path_test)
    dict=defaultdict(list)
    G = list(test[sens_attr_col].values)
    n = len(G)
    freq = Counter(G)
    sens_attr_values = np.unique(G)
    
    for _, row in test.iterrows():
        bucket = query([row[column[0]],row[column[1]]], f, scores, 2, num_of_buckets)
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
    
    

def fit_predict_eval_input(path_train, path_test,n_vectors, column,sens_attr_col,num_of_buckets):
    dataset = read_file(path_train, column)
    f = polartoscalar([0], 2)
    scores = sorted([score(dataset[i], f, 2) for i in range(len(dataset))])
    
    test=pd.read_csv(path_test)
    dict=defaultdict(list)
    G = list(test[sens_attr_col].values)
    n = len(G)
    freq = Counter(G)
    sens_attr_values = np.unique(G)
    
    for _, row in test.iterrows():
        bucket = query([row[column[0]],row[column[1]]], f, scores, 2, num_of_buckets)
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
