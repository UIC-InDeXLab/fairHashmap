import numpy as np

from hybrid_with_sampling import generate_sample, hybrid_with_sampling
from ranking_2d import query
from utils import read_file, polartoscalar, score

queries = []
for i in range(100):
    query_x = np.random.uniform(0, 1)
    query_y = np.random.uniform(0, 1)
    queries.append([query_x, query_y])

path = "synthetic_data/2d_sample_0.2_1000.csv"
number_of_buckets = 20
d = 2
sample = generate_sample(path, d, number_of_buckets, "S")
theta_1, theta_2 = hybrid_with_sampling(path, sample, ["X1", "X2"], number_of_buckets, "S")
dataset = read_file(path, ["X1", "X2"])
f = polartoscalar([theta_1], d)
scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])
print(query(queries[0], f, scores, d, number_of_buckets))

f = polartoscalar([theta_2], d)
scores = sorted([score(dataset[i], f, d) for i in range(len(dataset))])
print(query(queries[0], f, scores, d, number_of_buckets))
