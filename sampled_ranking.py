import math
import numpy as np
import pandas as pd
from ranking import basestuff_, TwoD_
from ultimate_alg import necklace_split


def sampled_ranking(df_sampled, path, number_of_buckets):
    n = df_sampled.shape[0]
    basestuff_.setparams(n, 2)
    basestuff_.genDataDf(df_sampled)
    basestuff_.genDataDf_(path)
    number_of_cuts = []
    for i in range(n * n):  # Ask??
        print(i, "th iteration of", n * n)
        s, r, theta = TwoD_.GetNext()
        if s is None:
            break
        _, boundary, _, ordering = necklace_split(path, r[1], "X1", "S", ["F", "M"], number_of_buckets)
        number_of_cuts.append(len(boundary))
        print("min cut #:", sorted(number_of_cuts)[0])
        print("---------------------------------------------------")
    return sorted(number_of_cuts)


path = "data/2d_sample_0.2_1000.csv"
df = pd.read_csv(path)
n = df.shape[0]
m = 10
d = 2
print(int(np.ceil(12 * m * d * math.log(n) / 50)))
df_M = df[df['S'] == 'M'].sample(int(np.ceil(12 * m * d * math.log(n) / 50)))
df_F = df[df['S'] == 'F'].sample(int(np.ceil(12 * m * d * math.log(n) / 50)))
df_sampled = pd.concat([df_M, df_F], axis=0).sample(frac=1.0).reset_index()
print(sampled_ranking(df_sampled, path, number_of_buckets=m))

# n=1000, ratio=0.2, m=50, 83 from each group, total of 166 samples, min number of cuts 76
# n=1000, ratio=0.2, m=30, 100 from each group, total of 200 samples, min number of cuts 47
# n=1000, ratio=0.2, m=10, 34 from each group, total of 68 samples, min number of cuts 12
# n=10000, ratio=0.2, m=50, 222 from each group, total of 444 samples, min number of cuts 87
