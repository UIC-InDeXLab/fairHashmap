import timeit

import numpy as np
import pandas as pd
from ranking_util import basestuff, TwoD
from necklace_split_binary import necklace_split


def hybrid_with_no_sampling(path, sens_attr, columns, number_of_buckets):
    G = list(pd.read_csv(path)[sens_attr].values)
    n = len(G)
    basestuff.read_file(file=path, columns=columns)
    number_of_cuts = []
    boundary_indices = []
    boundaries = []
    hash_buckets = []
    Theta = []
    start = timeit.default_timer()
    for i in range(n * n):
        r, j, theta = TwoD.GetNext()
        if r is not None and j != -1:
            idx1 = r[j]
            idx2 = r[j + 1]
            if i == 0 or (idx2 in boundary_indices and G[idx1] != G[idx2]):
                F = necklace_split(path, columns, sens_attr, number_of_buckets, r, theta)
                boundary_indices = F[0]
                boundaries.append(F[1])
                hash_buckets.append((F[2]))
                number_of_cuts.append(len(F[1]))
                Theta.append(theta)
        elif r is not None and j == -1:
            F = necklace_split(path, columns, sens_attr, number_of_buckets, r, theta)
            boundary_indices = F[0]
            boundaries.append(F[1])
            hash_buckets.append((F[2]))
            number_of_cuts.append(len(F[1]))
            Theta.append(theta)
        else:
            break
    stop = timeit.default_timer()
    return number_of_cuts[np.min(number_of_cuts)], boundaries[np.min(number_of_cuts)], hash_buckets[
        np.min(number_of_cuts)], Theta[np.min(number_of_cuts)], stop-start
