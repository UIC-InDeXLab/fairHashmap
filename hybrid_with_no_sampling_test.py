import numpy as np
from hybrid_with_no_sampling import hybrid_with_no_sampling
from necklace_split_binary import query

queries = []
for i in range(100):
    query_x = np.random.uniform(0, 1)
    query_y = np.random.uniform(0, 1)
    queries.append([query_x, query_y])

path = "synthetic_data/2d_sample_0.2_100.csv"
number_of_buckets = 10
num_of_cuts, boundary, hash_buckets = hybrid_with_no_sampling(path, "S", ["X1", "X2"], number_of_buckets)
print(queries[0][0])
print(boundary)
print(hash_buckets)
print(query(queries[0][0], boundary, hash_buckets))
