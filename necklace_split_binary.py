import itertools
import timeit
from bisect import bisect

import numpy as np
import pandas as pd
from collections import defaultdict, Counter
from scipy.special import comb

from utils import polartoscalar


def necklace_split(
    path, columns, sens_attr_col, num_of_buckets, ranking=None, theta=None, d=2
):
    df = pd.read_csv(path)
    if ranking is not None:
        G = [list(df[sens_attr_col].values)[i] for i in ranking]
        G.reverse()
        f = polartoscalar([theta], d)
        T = [
            list(df[columns[0]].values)[i] * f[0]
            + list(df[columns[1]].values)[i] * f[1]
            for i in ranking
        ]
        T.reverse()
    else:
        df = df.sort_values(columns[0])
        G = list(df[sens_attr_col].values)
        G_ = list(df[sens_attr_col].values)
        T = list(df[columns[0]].values)
    start = timeit.default_timer()
    size = df.shape[0]
    sens_attr_values = np.unique(G)
    c_F_total = G.count(sens_attr_values[0])
    c_M_total = G.count(sens_attr_values[1])
    n = len(G)
    freq = Counter(G_)
    indices = [i for i in range(n)]
    arc_size = int(np.ceil((c_F_total + c_M_total) / num_of_buckets))
    hash_buckets = [None for _ in range(size)]
    boundary = []
    offset = 0
    RR=[]
    for j in range(num_of_buckets):
        if offset + arc_size <= n:
            c_F_ = G[offset : arc_size + offset].count(sens_attr_values[0])
            c_M_ = G[offset : arc_size + offset].count(sens_attr_values[1])
        else:
            if offset <= n:
                c_F_ = list(
                    itertools.chain(G[offset:n], G[: (offset + arc_size) % n])
                ).count(sens_attr_values[0])
                c_M_ = list(
                    itertools.chain(G[offset:n], G[: (offset + arc_size) % n])
                ).count(sens_attr_values[1])
            else:
                if offset % n <= (offset + arc_size) % n:
                    c_F_ = G[offset % n : (offset + arc_size) % n].count(
                        sens_attr_values[0]
                    )
                    c_M_ = G[offset % n : (offset + arc_size) % n].count(
                        sens_attr_values[1]
                    )
                else:
                    c_F_ = list(
                        itertools.chain(G[offset % n : n], G[: (offset + arc_size) % n])
                    ).count(sens_attr_values[0])
                    c_M_ = list(
                        itertools.chain(G[offset % n : n], G[: (offset + arc_size) % n])
                    ).count(sens_attr_values[1])

        # print('starting counts:', c_F_, c_M_)
        # print('G', G)
        # print('indices', indices)
        for i in range(n):
            if i + offset != offset:
                if i + offset + arc_size <= n:
                    if (
                        G[i + offset - 1] == sens_attr_values[0]
                        and G[i + offset + arc_size - 1] == sens_attr_values[1]
                    ):
                        c_F_ -= 1
                        c_M_ += 1
                    if (
                        G[i + offset - 1] == sens_attr_values[1]
                        and G[i + offset + arc_size - 1] == sens_attr_values[0]
                    ):
                        c_F_ += 1
                        c_M_ -= 1
                    # print(c_F_, c_M_, G[i + offset:i + offset + arc_size], indices[i + offset:i + offset + arc_size])
                else:
                    if i + offset <= n:
                        if (
                            G[i + offset - 1] == sens_attr_values[0]
                            and G[(i + offset + arc_size) % n - 1]
                            == sens_attr_values[1]
                        ):
                            c_F_ -= 1
                            c_M_ += 1
                        if (
                            G[i + offset - 1] == sens_attr_values[1]
                            and G[(i + offset + arc_size) % n - 1]
                            == sens_attr_values[0]
                        ):
                            c_F_ += 1
                            c_M_ -= 1
                        # print(c_F_, c_M_, list(itertools.chain(G[i + offset:n], G[:(i + offset + arc_size) % n])),
                        #       indices[i + offset:n] + indices[:(i + offset + arc_size) % n])
                    else:
                        if (i + offset) % n <= (i + offset + arc_size) % n:
                            if (
                                G[(i + offset) % n - 1] == sens_attr_values[0]
                                and G[(i + offset + arc_size) % n - 1]
                                == sens_attr_values[1]
                            ):
                                c_F_ -= 1
                                c_M_ += 1
                            if (
                                G[(i + offset) % n - 1] == sens_attr_values[1]
                                and G[(i + offset + arc_size) % n - 1]
                                == sens_attr_values[0]
                            ):
                                c_F_ += 1
                                c_M_ -= 1
                            # print(c_F_, c_M_, G[(i + offset) % n:(i + offset + arc_size) % n],
                            #       indices[(i + offset) % n:(i + offset + arc_size) % n])

                        else:
                            if (
                                G[(i + offset + arc_size) % n - 1]
                                == sens_attr_values[1]
                                and G[(i + offset) % n - 1] == sens_attr_values[0]
                            ):
                                c_F_ += 1
                                c_M_ -= 1
                            if (
                                G[(i + offset + arc_size) % n - 1]
                                == sens_attr_values[0]
                                and G[(i + offset) % n - 1] == sens_attr_values[1]
                            ):
                                c_F_ -= 1
                                c_M_ += 1
                            # print(c_F_, c_M_,
                            #       list(itertools.chain(G[(i + offset) % n:n], G[:(i + offset + arc_size) % n])),
                            #       indices[(i + offset) % n:n] + indices[:(i + offset + arc_size) % n])

            if c_F_ == int(np.ceil(c_F_total / num_of_buckets)) and c_M_ == int(
                np.ceil(c_M_total / num_of_buckets)-1
            ):
                break
        if i + offset + arc_size < n:
            if i + offset != 0 and i + offset != size:
                boundary.append(indices[i + offset])
                boundary.append(indices[i + offset + arc_size])
                for idx in range(i + offset, i + offset + arc_size):
                    hash_buckets[indices[idx]]=j
                # hash_buckets.extend([j, j])
                RR.append(G[i + offset: i + offset + arc_size])
                # print(Counter(G[i + offset: i + offset + arc_size]))
            # if i + offset == offset:
            #     print(c_F_, c_M_, G[i + offset: i + offset + arc_size], indices[i + offset: i + offset + arc_size])
            del G[i + offset : i + offset + arc_size]
            del indices[i + offset : i + offset + arc_size]
            if n != 0:
                offset = (offset + i) % n
        else:
            if i + offset < n:
                if i + offset != 0 and i + offset != size:
                    boundary.append(indices[i + offset])
                    boundary.append(indices[(i + offset + arc_size) % n])
                    # hash_buckets.extend([j, j])
                    for idx in range(i + offset, n):
                        hash_buckets[indices[idx]]=j
                    for idx in range((i + offset + arc_size) % n):
                        hash_buckets[indices[idx]]=j
                    RR.append(G[i + offset: n] + G[:(i + offset + arc_size) % n])
                    # print(Counter(G[i + offset: n] + G[:(i + offset + arc_size) % n]))
                # if i + offset == offset:
                #     print(c_F_, c_M_, G[i + offset: n] + G[:(i + offset + arc_size) % n],
                #           indices[i + offset: n] + indices[:(i + offset + arc_size) % n])
                del G[i + offset : n], G[: (i + offset + arc_size) % n]
                del indices[i + offset : n], indices[: (i + offset + arc_size) % n]
                offset = 0
            else:
                if (i + offset) % n < (i + offset + arc_size) % n:
                    if (i + offset) % n > 0 and (
                        i + offset
                    ) % n != size:  # used to be !=0 changed it to >0, check if ok
                        boundary.append(indices[(i + offset) % n])
                        boundary.append(indices[(i + offset + arc_size) % n])
                        # hash_buckets.extend([j, j])
                        for idx in range((i + offset) % n , (i + offset + arc_size) % n):
                            hash_buckets[indices[idx]]=j
                        RR.append(G[(i + offset) % n : (i + offset + arc_size) % n])
                        # print(Counter(G[(i + offset) % n:(i + offset + arc_size) % n]))
                    # if i + offset == offset:
                    #     print(c_F_, c_M_, G[(i + offset) % n:(i + offset + arc_size) % n],
                    #           indices[(i + offset) % n:(i + offset + arc_size) % n])
                    del G[(i + offset) % n : (i + offset + arc_size) % n]
                    del indices[(i + offset) % n : (i + offset + arc_size) % n]
                    offset = (i + offset) % n
                else:
                    if (i + offset) % n > 0 and (i + offset) % n != size:
                        boundary.append(indices[(i + offset) % n])
                        boundary.append(indices[(i + offset + arc_size) % n])
                        # hash_buckets.extend([j, j])
                        for idx in range((i + offset) % n , n):
                            hash_buckets[indices[idx]]=j
                        for idx in range((i + offset + arc_size) % n):
                            hash_buckets[indices[idx]]=j
                    # if i + offset == offset:
                    #     print(c_F_, c_M_, G[(i + offset) % n:n], G[:(i + offset + arc_size) % n],
                    #           indices[(i + offset) % n:n] + indices[:(i + offset + arc_size) % n])
                    RR.append(G[(i + offset) % n:n]+ G[:(i + offset + arc_size) % n])
                    # print(Counter(G[(i + offset) % n:(i + offset + arc_size) % n]))
                    del G[(i + offset) % n : n], G[: (i + offset + arc_size) % n]
                    del (
                        indices[(i + offset) % n : n],
                        indices[: (i + offset + arc_size) % n],
                    )
                    offset = (i + offset) % n
        n = n - arc_size
        # print('offset', offset)
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            
    
    stop = timeit.default_timer()
    # print(hash_buckets)
    hs=[hash_buckets[0]]
    tmp=hash_buckets[0]
    for idx in range(1,len(hash_buckets)):
        if hash_buckets[idx]==tmp:
            tmp=hash_buckets[idx]
            continue
        tmp=hash_buckets[idx]
        hs.append(hash_buckets[idx])
    
    zipped_hash=sorted(zip(np.unique(boundary), hs), key=lambda x: x[0])
    return (
        np.unique(sorted(boundary)),
        [T[key] for key,val in zipped_hash],
        [val for key, val in zipped_hash],
        stop - start,
    )


def query(q, boundary, hash_buckets,  theta=None, d=2):
    if theta is not None:
        f = polartoscalar(theta, d)
        q = f[0] * q[0] + f[1] * q[1]
    idx = bisect(boundary, q)
    if idx == len(hash_buckets):
        return hash_buckets[-1]
    else:
        return hash_buckets[idx]
    

def fit_predict_eval_necklace(path_train, path_test, column,sens_attr_col,num_of_buckets):
    _, boundary, hash_buckets,_=necklace_split(path_train,column,sens_attr_col,num_of_buckets)
    test=pd.read_csv(path_test)
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
        # print(len(bucket),len(dict.keys()),Counter(bucket))
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
    single_fairness= (max_collision_prob_single / min_collision_prob_single) - 1
            
    max_collision_prob_pairwise = np.max(
        [collision_prob_pairwise[sens_attr] for sens_attr in sens_attr_values]
    )
    min_collision_prob_pairwise = np.min(
        [collision_prob_pairwise[sens_attr] for sens_attr in sens_attr_values]
    )
    
    pairwise_fairness= (max_collision_prob_pairwise / min_collision_prob_pairwise) - 1
    
    return collision_prob, single_fairness, pairwise_fairness
    # return collision_prob, collision_prob_single, collision_prob_pairwise
        
        
