from necklace_split_binary import fit_predict_eval_necklace
from ranking_sampled_vector import fit_predict_eval, fit_predict_eval_input
from sweep_and_cut import fit_predict_eval_sweep

m=100
nv=100

print("adult, input:",fit_predict_eval_input("real_data/train_test/adult_train.csv","real_data/train_test/adult_test.csv",nv,["fnlwgt", "education-num"],"sex",m))
print("compas, input:",fit_predict_eval_input("real_data/train_test/compas_random_id_train.csv","real_data/train_test/compas_random_id_test.csv",nv,["ID", "RawScore"],"Sex_Code_Text",m))
print("diabetes, input:",fit_predict_eval_input("real_data/train_test/diabetes_train.csv","real_data/train_test/diabetes_test.csv",nv,["encounter_id", "patient_nbr"],"gender",m))
print("popsim, input:",fit_predict_eval_input("real_data/train_test/popsim_binary_train.csv","real_data/train_test/popsim_binary_test.csv",nv,["lat", "lon"],"race",m))

print("adult, sampled ranking:",fit_predict_eval("real_data/train_test/adult_train.csv","real_data/train_test/adult_test.csv",nv,["fnlwgt", "education-num"],"sex",nv))
print("compas, sampled ranking:",fit_predict_eval("real_data/train_test/compas_random_id_train.csv","real_data/train_test/compas_random_id_test.csv",nv,["ID", "RawScore"],"Sex_Code_Text",nv))
print("diabetes, sampled ranking:",fit_predict_eval("real_data/train_test/diabetes_train.csv","real_data/train_test/diabetes_test.csv",nv,["encounter_id", "patient_nbr"],"gender",nv))
print("popsim, sampled ranking:",fit_predict_eval("real_data/train_test/popsim_binary_train.csv","real_data/train_test/popsim_binary_test.csv",nv,["lat", "lon"],"race",nv))

print("adult, necklacesplitting:",fit_predict_eval_necklace("real_data/train_test/adult_train.csv","real_data/train_test/adult_test.csv",["fnlwgt", "education-num"],"sex",m))
print("compas, necklacesplitting:",fit_predict_eval_necklace("real_data/train_test/compas_random_id_train.csv","real_data/train_test/compas_random_id_test.csv",["ID", "RawScore"],"Sex_Code_Text",m))
print("diabetes, necklacesplitting:",fit_predict_eval_necklace("real_data/train_test/diabetes_train.csv","real_data/train_test/diabetes_test.csv",["encounter_id", "patient_nbr"],"gender",m))
print("popsim, necklacesplitting:",fit_predict_eval_necklace("real_data/train_test/popsim_binary_train.csv","real_data/train_test/popsim_binary_test.csv",["lon", "lat"],"race",m))

print("adult, sweep and cut:",fit_predict_eval_sweep("real_data/train_test/adult_train.csv","real_data/train_test/adult_test.csv",["fnlwgt", "education-num"],"sex",m))
print("compas, sweep and cut:",fit_predict_eval_sweep("real_data/train_test/compas_random_id_train.csv","real_data/train_test/compas_random_id_test.csv",["ID", "RawScore"],"Sex_Code_Text",m))
print("diabetes, sweep and cut:",fit_predict_eval_sweep("real_data/train_test/diabetes_train.csv","real_data/train_test/diabetes_test.csv",["encounter_id", "patient_nbr"],"gender",m))
print("popsim, sweep and cut:",fit_predict_eval_sweep("real_data/train_test/popsim_binary_train.csv","real_data/train_test/popsim_binary_test.csv",["lon", "lat"],"race",m))

