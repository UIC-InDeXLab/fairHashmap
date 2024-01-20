import math
import numpy as np
from utils import rank, read_file
import timeit
from copy import deepcopy
from necklace_split_binary import necklace_split


def hybrid(path, n_vectors, sens_attr, columns, number_of_buckets):
    Theta=list(np.random.uniform(low=0,high=math.pi / 2, size=n_vectors))
    Theta.insert(0,0)
    dataset=read_file(path,columns)
    boundaries=[]
    hash_buckets=[]
    number_of_cuts=[]
    start = timeit.default_timer()
    for theta in Theta:
        r=deepcopy(rank(dataset,[theta],2))
        F = necklace_split(
                    path, columns, sens_attr, number_of_buckets, r, theta
                )
        boundaries.append(F[1])
        hash_buckets.append((F[2]))
        number_of_cuts.append(len(F[1]))
    stop = timeit.default_timer()
    return number_of_cuts[np.argmin(number_of_cuts)], boundaries[np.argmin(number_of_cuts)], hash_buckets[np.argmin(number_of_cuts)], Theta[np.argmin(number_of_cuts)], stop - start