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
    df.to_csv("synthetic_data/" + file_name)



