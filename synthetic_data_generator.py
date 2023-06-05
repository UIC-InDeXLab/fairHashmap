import random
import numpy as np
import pandas as pd


def generate_2D_data(file_name, n, minority_count):
    majority_count = n - minority_count
    df = pd.DataFrame(np.random.uniform(0, 1, size=(n, 2)), columns=["X1", "X2"])
    s = []
    for i in range(minority_count):
        s.append("F")
    for i in range(majority_count):
        s.append("M")
    random.shuffle(s)
    df["S"] = s
    df.to_csv("data/" + file_name)

generate_2D_data("2d_sample_0.2_100.csv", n=100, minority_count=20)

# generate_2D_data("2d_sample_0.1_1000.csv", n=1000, minority_count=100)
# generate_2D_data("2d_sample_0.1_10000.csv", n=10000, minority_count=1000)
# generate_2D_data("2d_sample_0.1_100000.csv", n=100000, minority_count=10000)
# generate_2D_data("2d_sample_0.1_1000000.csv", n=1000000, minority_count=100000)
# generate_2D_data("2d_sample_0.1_10000000.csv", n=10000000, minority_count=1000000)
#
#
# generate_2D_data("2d_sample_0.2_1000.csv", n=1000, minority_count=200)
# generate_2D_data("2d_sample_0.2_10000.csv", n=10000, minority_count=2000)
# generate_2D_data("2d_sample_0.2_100000.csv", n=100000, minority_count=20000)
# generate_2D_data("2d_sample_0.2_1000000.csv", n=1000000, minority_count=200000)
# generate_2D_data("2d_sample_0.2_10000000.csv", n=10000000, minority_count=2000000)
#
#
# generate_2D_data("2d_sample_0.3_1000.csv", n=1000, minority_count=300)
# generate_2D_data("2d_sample_0.3_10000.csv", n=10000, minority_count=3000)
# generate_2D_data("2d_sample_0.3_100000.csv", n=100000, minority_count=30000)
# generate_2D_data("2d_sample_0.3_1000000.csv", n=1000000, minority_count=300000)
# generate_2D_data("2d_sample_0.3_10000000.csv", n=10000000, minority_count=3000000)
#
#
# generate_2D_data("2d_sample_0.4_1000.csv", n=1000, minority_count=400)
# generate_2D_data("2d_sample_0.4_10000.csv", n=10000, minority_count=4000)
# generate_2D_data("2d_sample_0.4_100000.csv", n=100000, minority_count=40000)
# generate_2D_data("2d_sample_0.4_1000000.csv", n=1000000, minority_count=400000)
# generate_2D_data("2d_sample_0.4_10000000.csv", n=10000000, minority_count=4000000)
#
#
# generate_2D_data("2d_sample_0.5_1000.csv", n=1000, minority_count=500)
# generate_2D_data("2d_sample_0.5_10000.csv", n=10000, minority_count=5000)
# generate_2D_data("2d_sample_0.5_100000.csv", n=100000, minority_count=50000)
# generate_2D_data("2d_sample_0.5_1000000.csv", n=1000000, minority_count=500000)
# generate_2D_data("2d_sample_0.5_10000000.csv", n=10000000, minority_count=5000000)

