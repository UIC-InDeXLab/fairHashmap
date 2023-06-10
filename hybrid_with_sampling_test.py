from hybrid_with_sampling import generate_sample, hybrid_with_sampling

path = "synthetic_data/2d_sample_0.2_1000.csv"
sample = generate_sample(path, 2, 10, "S")
hybrid_with_sampling(path, sample, ["X1", "X2"], 10, "S")
