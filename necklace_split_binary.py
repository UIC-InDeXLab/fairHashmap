import itertools
import timeit
from bisect import bisect
import numpy as np
import pandas as pd
from utils import polartoscalar, score


def necklace_split(path, col, sens_attr_col, num_of_buckets, ranking=None, theta=None, d=2):
    df = pd.read_csv(path)
    if ranking is not None:
        G = [list(df[sens_attr_col].values)[i] for i in ranking]
        G.reverse()
        f = polartoscalar([theta], d)
        T = [list(df[col].values)[i] * f[0] + list(df["X2"].values)[i] * f[1] for i in ranking]
        T.reverse()
    else:
        df = df.sort_values(col)
        G = list(df[sens_attr_col].values)
        T = list(df[col].values)
    start = timeit.default_timer()
    size = df.shape[0]
    sens_attr_values = np.unique(G)
    c_F_total = G.count(sens_attr_values[0])
    c_M_total = G.count(sens_attr_values[1])
    n = len(G)
    indices = [i for i in range(n)]
    arc_size = int(np.ceil((c_F_total + c_M_total) / num_of_buckets))
    hash_buckets = []
    boundary = []
    offset = 0
    for j in range(num_of_buckets):
        if offset + arc_size <= n:
            c_F_ = G[offset: arc_size + offset].count(sens_attr_values[0])
            c_M_ = G[offset: arc_size + offset].count(sens_attr_values[1])
        else:
            if offset <= n:
                c_F_ = list(itertools.chain(G[offset:n], G[:(offset + arc_size) % n])).count(sens_attr_values[0])
                c_M_ = list(itertools.chain(G[offset:n], G[:(offset + arc_size) % n])).count(sens_attr_values[1])
            else:
                if offset % n <= (offset + arc_size) % n:
                    c_F_ = G[offset % n:(offset + arc_size) % n].count(sens_attr_values[0])
                    c_M_ = G[offset % n:(offset + arc_size) % n].count(sens_attr_values[1])
                else:
                    c_F_ = list(itertools.chain(G[offset % n:n], G[:(offset + arc_size) % n])).count(
                        sens_attr_values[0])
                    c_M_ = list(itertools.chain(G[offset % n:n], G[:(offset + arc_size) % n])).count(
                        sens_attr_values[1])

        # print('starting counts:', c_F_, c_M_)
        # print('G', G)
        # print('indices', indices)
        for i in range(n):
            if i + offset != offset:
                if i + offset + arc_size <= n:
                    if G[i + offset - 1] == sens_attr_values[0] and G[i + offset + arc_size - 1] == sens_attr_values[1]:
                        c_F_ -= 1
                        c_M_ += 1
                    if G[i + offset - 1] == sens_attr_values[1] and G[i + offset + arc_size - 1] == sens_attr_values[0]:
                        c_F_ += 1
                        c_M_ -= 1
                    # print(c_F_, c_M_, G[i + offset:i + offset + arc_size], indices[i + offset:i + offset + arc_size])
                else:
                    if i + offset <= n:
                        if G[i + offset - 1] == sens_attr_values[0] and G[(i + offset + arc_size) % n - 1] == \
                                sens_attr_values[1]:
                            c_F_ -= 1
                            c_M_ += 1
                        if G[i + offset - 1] == sens_attr_values[1] and G[(i + offset + arc_size) % n - 1] == \
                                sens_attr_values[0]:
                            c_F_ += 1
                            c_M_ -= 1
                        # print(c_F_, c_M_, list(itertools.chain(G[i + offset:n], G[:(i + offset + arc_size) % n])),
                        #       indices[i + offset:n] + indices[:(i + offset + arc_size) % n])
                    else:
                        if (i + offset) % n <= (i + offset + arc_size) % n:

                            if G[(i + offset) % n - 1] == sens_attr_values[0] and G[(i + offset + arc_size) % n - 1] == \
                                    sens_attr_values[1]:
                                c_F_ -= 1
                                c_M_ += 1
                            if G[(i + offset) % n - 1] == sens_attr_values[1] and G[(i + offset + arc_size) % n - 1] == \
                                    sens_attr_values[0]:
                                c_F_ += 1
                                c_M_ -= 1
                            # print(c_F_, c_M_, G[(i + offset) % n:(i + offset + arc_size) % n],
                            #       indices[(i + offset) % n:(i + offset + arc_size) % n])

                        else:
                            if G[(i + offset + arc_size) % n - 1] == sens_attr_values[1] and G[(i + offset) % n - 1] == \
                                    sens_attr_values[0]:
                                c_F_ += 1
                                c_M_ -= 1
                            if G[(i + offset + arc_size) % n - 1] == sens_attr_values[0] and G[(i + offset) % n - 1] == \
                                    sens_attr_values[1]:
                                c_F_ -= 1
                                c_M_ += 1
                            # print(c_F_, c_M_,
                            #       list(itertools.chain(G[(i + offset) % n:n], G[:(i + offset + arc_size) % n])),
                            #       indices[(i + offset) % n:n] + indices[:(i + offset + arc_size) % n])

            if c_F_ == int(np.ceil(c_F_total / num_of_buckets)) and c_M_ == int(np.ceil(c_M_total / num_of_buckets)):
                break
        if i + offset + arc_size < n:
            if i + offset != 0 and i + offset != size:
                boundary.append(indices[i + offset])
                boundary.append(indices[i + offset + arc_size])
                hash_buckets.extend([j, j])
            # if i + offset == offset:
            #     print(c_F_, c_M_, G[i + offset: i + offset + arc_size], indices[i + offset: i + offset + arc_size])
            del G[i + offset: i + offset + arc_size]
            del indices[i + offset: i + offset + arc_size]
            if n != 0:
                offset = (offset + i) % n
        else:
            if i + offset < n:
                if i + offset != 0 and i + offset != size:
                    boundary.append(indices[i + offset])
                    boundary.append(indices[(i + offset + arc_size) % n])
                    hash_buckets.extend([j, j])
                # if i + offset == offset:
                #     print(c_F_, c_M_, G[i + offset: n] + G[:(i + offset + arc_size) % n],
                #           indices[i + offset: n] + indices[:(i + offset + arc_size) % n])
                del G[i + offset: n], G[:(i + offset + arc_size) % n]
                del indices[i + offset: n], indices[:(i + offset + arc_size) % n]
                offset = 0
            else:
                if (i + offset) % n < (i + offset + arc_size) % n:
                    if (i + offset) % n != 0 and (i + offset) % n != size:
                        boundary.append(indices[(i + offset) % n])
                        boundary.append(indices[(i + offset + arc_size) % n])
                        hash_buckets.extend([j, j])
                    # if i + offset == offset:
                    #     print(c_F_, c_M_, G[(i + offset) % n:(i + offset + arc_size) % n],
                    #           indices[(i + offset) % n:(i + offset + arc_size) % n])
                    del G[(i + offset) % n:(i + offset + arc_size) % n]
                    del indices[(i + offset) % n:(i + offset + arc_size) % n]
                    offset = (i + offset) % n
                else:
                    if (i + offset) % n != 0 and (i + offset) % n != size:
                        boundary.append(indices[(i + offset) % n])
                        boundary.append(indices[(i + offset + arc_size) % n])
                        hash_buckets.extend([j, j])
                    # if i + offset == offset:
                    #     print(c_F_, c_M_, G[(i + offset) % n:n], G[:(i + offset + arc_size) % n],
                    #           indices[(i + offset) % n:n] + indices[:(i + offset + arc_size) % n])
                    del G[(i + offset) % n:n], G[:(i + offset + arc_size) % n]
                    del indices[(i + offset) % n:n], indices[:(i + offset + arc_size) % n]
                    offset = (i + offset) % n
        n = n - arc_size
        # print('offset', offset)
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    stop = timeit.default_timer()
    return np.unique(sorted(boundary)), [T[val] for val in np.unique(sorted(boundary), return_index=True)[0]], \
        [hash_buckets[idx] for idx in np.unique(sorted(boundary), return_index=True)[1]], stop - start


def query(q, boundary, hash_buckets, theta=None, d=2):
    if theta is not None:
        f = polartoscalar(theta, d)
        q = f[0] * q[0] + f[1] * q[1]
    idx = bisect(boundary, q)
    if idx == len(hash_buckets):
        return hash_buckets[-1]
    else:
        return hash_buckets[idx]
