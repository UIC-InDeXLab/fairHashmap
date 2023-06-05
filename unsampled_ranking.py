import pandas as pd
from ranking import basestuff, TwoD
from ultimate_alg import necklace_split


def unsampled_ranking(path, sens_attr, sens_attr_values, number_of_buckets):
    G = list(pd.read_csv(path)[sens_attr].values)
    fileprefix = path
    n = len(G)
    basestuff.setparams(n, 2)
    basestuff.genData(file=fileprefix, pythonfile=False, cols=[1, 2], tuplenames=[1], header=1)
    number_of_cuts = []
    boundary = []
    for i in range(n * n):
        r, j = TwoD.GetNext()
        if r is not None and j != -1:
            idx1 = r[j]
            idx2 = r[j + 1]
            with open('res', 'a') as f:
                f.write("ith ranking: " + str(i) + '\n')
                f.write("swap happening at:" + str((idx1, idx2)) + '\n')
                f.write("boundary:" + str(boundary) + '\n')
                f.write(str(r) + '\n')
                f.write("-----------------------------------------------\n")
            if i == 0 or (idx2 in boundary and G[idx1] != G[idx2]):
                _, _, _, _, boundary = necklace_split(path, r, "X1", "S", ["F", "M"], number_of_buckets)
                number_of_cuts.append(len(boundary))
        elif r is not None and j == -1:
            _, _, _, _, boundary = necklace_split(path, r, "X1", "S", ["F", "M"], number_of_buckets)
        else:
            break

    return sorted(number_of_cuts)


path = "data/2d_sample_0.2_1000.csv"
number_of_buckets = 100
res = unsampled_ranking(path, "S", ["F", "M"], number_of_buckets)
print(len(res), res)

# 1) Theta values (theta1+theta2)/2 is not sorted, so there are multiple changes at each iteration. (it's not like
# ranking r[i] and r[i+1] are only different in a pair of swapped element)
# 2) which idx value should be in the boundary list? am I returning the right idx?
# 3) idx value should be in which boundary? only the boundary for the previous iteration (vector)?
# 4) should # of iterations be n*n?
