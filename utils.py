import math
import random
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def generate_synthetic_2D_data(file_name, n, minority_count):
    majority_count = n - minority_count
    df = pd.DataFrame(np.random.uniform(0, 1, size=(n, 2)), columns=["X1", "X2"])
    s = []
    for i in range(minority_count):
        s.append("F")
    for i in range(majority_count):
        s.append("M")
    random.shuffle(s)
    df["S"] = s
    df.to_csv("synthetic_data/" + file_name, index=False)


def generate_sample_of_size(path, dataset, n):
    df = pd.read_csv(path).sample(n)
    Path("real_data/" + dataset).mkdir(parents=True, exist_ok=True)
    df.to_csv("real_data/" + dataset + "/" + dataset + "_n_" + n + ".csv", index=False)


def generate_sample_of_fraction(path, dataset, f):
    df = pd.read_csv(path).sample(frac=f)
    Path("real_data/" + dataset).mkdir(parents=True, exist_ok=True)
    df.to_csv(
        "real_data/" + dataset + "/" + dataset + "_f_" + str(f) + ".csv", index=False
    )


def generate_sample_of_ratio(path, dataset, minority, majority, sens_attr):
    df = pd.read_csv(path)
    df_female = df[df[sens_attr] == "Female"].sample(minority)
    df_male = df[df[sens_attr] == "Male"].sample(majority)
    df_merged = pd.concat([df_male, df_female], ignore_index=True)
    Path("real_data/" + dataset).mkdir(parents=True, exist_ok=True)
    df_merged.to_csv(
        "real_data/"
        + dataset
        + "/"
        + dataset
        + "_r_"
        + str(float("{:.2f}".format((minority / majority))))
        + ".csv",
        index=False,
    )


def score(t, f, d):
    c = 0
    if len(f) != d:
        print("Error: Function length should be equal to d")
        return
    for j in range(d):
        c += f[j] * t[j]
    return c


def rank(dataset, theta, d):
    f = polartoscalar(theta, d)
    r = sorted(
        [[i, score(dataset[i], f, d)] for i in range(len(dataset))],
        key=lambda x: x[1],
        reverse=True,
    )
    return tuple([r[i][0] for i in range(len(r))])


def polartoscalar(theta, d, r=1):
    f = []
    for j in range(d - 1, 0, -1):
        f.insert(0, r * math.sin(theta[j - 1]))
        r *= math.cos(theta[j - 1])
    f.insert(0, r)
    return f


def read_file(file, columns):
    dataset = pd.read_csv(file)
    n = dataset.shape[0]
    d = 2
    dataset = dataset[[col for col in columns]]
    dataset["idx"] = [float(i) for i in range(dataset.shape[0])]
    dataset = dataset.to_numpy()
    return dataset


def plot(path, x_list, y_list, x_ticks, title, x_lable, y_lable):
    plt.figure()
    plt.plot(x_list, y_list)
    plt.xticks(x_ticks)
    plt.title(title)
    plt.xlabel(x_lable)
    plt.ylabel(y_lable)
    plt.ylim([100, 210])
    plt.savefig(path, dpi=300)


def plot_2(path, x_list, y1_list, y2_list, x_ticks, title, x_lable, y_lable):
    plt.figure()
    plt.plot(x_list, y1_list,label="number of cuts in practice")
    plt.plot(x_list, y2_list,label="upperbound (lemma 2)")
    plt.xticks(x_ticks)
    plt.title(title)
    plt.xlabel(x_lable)
    plt.ylabel(y_lable)
    plt.legend(loc="upper left")
    plt.savefig(path, dpi=300)
