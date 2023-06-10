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
    for i in range(n * n):
        r, j = TwoD.GetNext()
        if r is not None and j != -1:
            idx1 = r[j]
            idx2 = r[j + 1]
            if i == 0 or (idx2 in boundary_indices and G[idx1] != G[idx2]):
                boundary_indices, _, _, _ = necklace_split(path, columns[0], sens_attr, number_of_buckets, r)
                number_of_cuts.append(len(boundary_indices))
        elif r is not None and j == -1:
            boundary_indices, _, _, _ = necklace_split(path, columns[0], sens_attr, number_of_buckets, r)
        else:
            break
    return np.min(number_of_cuts)



