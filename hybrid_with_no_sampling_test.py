from hybrid_with_no_sampling import hybrid_with_no_sampling

path = "synthetic_data/2d_sample_0.2_100.csv"
number_of_buckets = 10
print(hybrid_with_no_sampling(path, "S", ["X1", "X2"], number_of_buckets))