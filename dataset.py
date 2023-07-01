from utils import generate_sample_of_fraction, generate_sample_of_ratio

datasets = ["adult", "compas"]
sens_attr = ["sex", "Sex_Code_Text"]
fractions = [0.2, 0.4, 0.6, 0.8, 1.0]
minority = [[4000, 8000, 12000, 16000], [3000, 6000, 9000, 12000]]
majority = [16000, 12000]
for idx in range(len(datasets)):
    for min_val in minority[idx]:
        generate_sample_of_ratio(
            "real_data/" + datasets[idx] + ".csv",
            datasets[idx],
            min_val,
            majority[idx],
            sens_attr[idx],
        )
    for frac in fractions:
        generate_sample_of_fraction(
            "real_data/" + datasets[idx] + ".csv", datasets[idx], frac
        )
