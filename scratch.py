import pandas as pd
import numpy as np
from ranking_sampled_vector import find_fair_ranking


# num_of_buckets = 10
# (
#     disparity,
#     disparity_original,
#     ranking,
#     theta,
#     duration,
# ) = find_fair_ranking("real_data/dummy.csv",10000, ["age", "education-num"], "sex", 10)
# print(disparity,disparity_original)

# df=pd.read_csv("real_data/popsim.csv")
# df=df[(df["race"]=="P1_003N") | (df["race"]=="P1_004N")]
# df[["race","lon","lat"]].to_csv("real_data/popsim_binary.csv", index=False)

# df=pd.read_csv("real_data/diabetes.csv")
# print(df["gender"].value_counts())

# df=pd.read_csv("real_data/compas.csv")
# df["ID"]=np.random.randint(10000,100000, df.shape[0])
# df.to_csv("real_data/compas_random_id.csv", index=False)


# datasets=["adult","compas_random_id","diabetes","popsim_binary"]
# for dataset in datasets:
#     df=pd.read_csv("real_data/"+dataset+"/"+dataset+"_r_0.25.csv")
#     train = df.sample(frac = 0.8, random_state = 200)
#     test=df.drop(train.index, errors='ignore', axis=0).sample(frac=1.0)
#     train.to_csv("real_data/train_test/"+dataset+"_train.csv",index=False)
#     test.to_csv("real_data/train_test/"+dataset+"_test.csv",index=False)



# print(pd.read_csv("real_data/compas.csv")["Ethnic_Code_Text"].value_counts())


# adult, input: (0.010362749999999993, 0.04397972116603266, 0.18887555600534012)
# compas, input: (0.010386888888888883, 0.0455716586151369, 0.1744083227665103)
# diabetes, input: (0.010123709629629631, 0.01290732933954608, 0.04126330880917539)
# popsim, input: (0.010049068888888894, 0.005910174329980533, 0.5659208467642804)

# adult, necklacesplitting: (0.019741124999999984, 0.026463168041066965, 0.00736078976745369)
# compas, necklacesplitting: (0.01876844444444445, 0.017204167425986627, 0.033116348326897915)
# diabetes, necklacesplitting: (0.020852890864197535, 0.005065654952415288, 0.006297912173977238)
# popsim, necklacesplitting: (0.010079795555555557, 0.01462663975782097, 0.0578896581171342)


    
arr=[[1.985922522842884, 3.9472888857126236, 0.31134066730737686, 7.944569766521454, 0.4466571509838104],
 [0.04517851024866104, 3.720202662050724, 5.572174981236458, 7.3937974870204926, 0.4170535057783127],
 [0.049505479633808136, 3.722967766225338, 5.61001306027174, 7.431792706251144, 0.4180167093873024],
 [0.05540137737989426, 3.868310682475567, 0.20828671008348465, 7.6872315257787704, 0.435522124171257],
 [0.05537649244070053, 3.5970859080553055, 0.2731066718697548, 7.170291893184185, 0.4079516977071762]]

arr3=[]
for i in range(5):
    arr2=[arr[j][i] for j in range(5)]
    arr3.append(np.mean(arr2))
print(arr3)