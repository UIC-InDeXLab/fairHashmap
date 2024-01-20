from utils import generate_sample_of_fraction, generate_sample_of_ratio
import pandas as pd

datasets = [
    # "adult", 
    # "compas_random_id",
    # "diabetes",
    "popsim_binary"
]
sens_attr = [
    # "sex", 
    # "Sex_Code_Text",
    # "gender",
    "race"
]
columns = [
    # ["fnlwgt", "education-num"],
    # ["ID", "RawScore"],
    # ["encounter_id", "patient_nbr"],
    ["lon", "lat"],
]
fractions = [0.2, 0.4, 0.6, 0.8, 1.0]
minority = [
    # [4000, 8000, 12000, 16000], 
    # [3000, 6000, 9000, 12000],
    # [11250, 22500 , 33750 , 45000],
    [30000, 60000, 90000, 120000]
    ]
majority = [
    # 16000, 
    # 12000, 
    # 45000, 
    120000
    ]
for idx in range(len(datasets)):
    # df=pd.read_csv("real_data/" + datasets[idx] + ".csv")
    # df[columns[idx][0]]=(df[columns[idx][0]]-df[columns[idx][0]].min())/(df[columns[idx][0]].max()-df[columns[idx][0]].min())
    # df[columns[idx][1]]=(df[columns[idx][1]]-df[columns[idx][1]].min())/(df[columns[idx][1]].max()-df[columns[idx][1]].min())
    # df.to_csv("real_data/" + datasets[idx] + ".csv",index=False)

    for min_val in minority[idx]:
        generate_sample_of_ratio(
            "real_data/" + datasets[idx] + ".csv",
            datasets[idx],
            min_val,
            majority[idx],
            sens_attr[idx],
        )
    # for frac in fractions:
    #     generate_sample_of_fraction(
    #         "real_data/" + datasets[idx] + ".csv", datasets[idx], frac
    #     )
