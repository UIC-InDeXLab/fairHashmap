from collections import Counter

import numpy as np
import pandas as pd


def Next(x):
    if np.ceil(x) == x:
        return x + 1
    else:
        return int(np.ceil(x))


def necklace_split(path, sens_attr_col, k):
    df = pd.read_csv(path)
    A = list(df[sens_attr_col].values)
    n = len(A)
    group_to_index_map = {}
    counter = 0
    for i in range(n):
        if A[i] in group_to_index_map.keys():
            A[i] = group_to_index_map[A[i]]
        else:
            group_to_index_map[A[i]] = counter
            A[i] = counter
            counter += 1
    J = []
    W = []
    n_c = Counter(A)
    for i in range(n):
        J.append((i, i + 1))
        W.append(1 / n_c[A[i]])
    x = 0
    I = []
    I_r = [0 for _ in range(k)]
    sum = 0
    while x < n:
        i = Next(x)
        w = (i - x) * W[i - 1]
        if sum + w < 0.5:
            sum = sum + w
            x = i
            a = A[i - 1]
            I_r[a] = I_r[a] + w
        else:
            delta = 0.5 - sum
            a = A[i - 1]
            I_r[a] = I_r[a] + delta
            x = x + delta / W[i - 1]
            I_r[k - 1] = x
            I.append(I_r)
            sum = 0
            I_r = [0 for _ in range(k)]
            I_r[0] = x
    print(I)
    scalars = np.linalg.solve(I[:3], [0.5 for _ in range(k)])
    return scalars


print(necklace_split("synthetic_data/2d_sample_100_3ary.csv", "S", 3))
