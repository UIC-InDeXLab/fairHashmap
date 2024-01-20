import pandas as pd
import math

def measure_cp(arr,boundaries):
    n=len(arr)
    cp=0
    for i in range(1,len(boundaries)):
        bucket_length= boundaries[i]-boundaries[i-1]
        cp+= (bucket_length/n)**2 
    return cp
        
    
def measure_sf(arr,boundaries):
    n=len(arr)
    sf_0=0
    sf_1=0
    total_0=arr.count(0)
    total_1=arr.count(1)
    for i in range(1,len(boundaries)):
        bucket=arr[boundaries[i-1]:boundaries[i]]
        count_0=bucket.count(0)
        count_1=bucket.count(1)
        bucket_length= boundaries[i]-boundaries[i-1]
        sf_0+=(count_0*bucket_length)/(total_0*n)
        sf_1+=(count_1*bucket_length)/(total_1*n)  
    return max(sf_0,sf_1)/min(sf_0,sf_1)-1
    
def measure_pf(arr,boundaries):
    pf_0=0
    pf_1=0
    total_0=arr.count(0)
    total_1=arr.count(1)
    for i in range(1,len(boundaries)):
        bucket=arr[boundaries[i-1]:boundaries[i]]
        count_0=bucket.count(0)
        count_1=bucket.count(1)
        pf_0+=(count_0/total_0)**2
        pf_1+=(count_1/total_1)**2  
    return max(pf_0,pf_1)/min(pf_0,pf_1)-1

arr = pd.read_pickle(r'ordering_diabetes.pkl')
m=100
n=len(arr)
bucket_size=n//m
boundaries=[i*bucket_size for i in range(m)]
boundaries.append(n)

max_iter=1000

sf_lb=0
sf_ub=0.05
cp_ub=0.1


F_total=[]
S_total=[]
C_total=[]

for i in range(max_iter):
    F=measure_pf(arr,boundaries)
    S=measure_sf(arr,boundaries)
    C=measure_cp(arr,boundaries)
    print(F,S)
    
    F_total.append(F)
    S_total.append(S)
    C_total.append(C)
    
    mF=math.inf
    j_star=0
    j_plus_minus=0
    for j in range(len(boundaries)):
        boundaries[j]=boundaries[j]-1
        F_=measure_pf(arr,boundaries)
        S_=measure_sf(arr,boundaries)
        C_=measure_cp(arr,boundaries)
        if F_<mF and sf_lb<=S_<=sf_ub and C_<=cp_ub:
            mF=F_
            j_star=j
            j_plus_minus="-"
        boundaries[j]=boundaries[j]+2
        F_=measure_pf(arr,boundaries)
        S_=measure_sf(arr,boundaries)
        C_=measure_cp(arr,boundaries)
        if F_<mF and sf_lb<=S_<=sf_ub and C_<=cp_ub:
            mF=F_
            j_star=j
            j_plus_minus="+"
        boundaries[j]=boundaries[j]-1
    if mF<F:
        if j_plus_minus=="-":
            boundaries[j_star]=boundaries[j_star]-1
        else:
            boundaries[j_star]=boundaries[j_star]+1
    else:
        break
    
index=[i+1 for i in range(104)]
# print(len(index),len(F_total),len(S_total),len(C_total))
# print(index)
# print(F_total)
# print(S_total)
# print(C_total)


print([index[i*10] for i in range(9)])
print([F_total[i*10] for i in range(9)])
print([S_total[i*10] for i in range(9)])
print([C_total[i*10] for i in range(9)])










