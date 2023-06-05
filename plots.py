import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (10, 5)

ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
sizes = [1000, 10000, 100000, 1000000, 10000000]
num_of_buckets = [10, 100, 1000, 10000, 100000]

varying_size_duration_necklace_splitting = [0.0029690039999999973, 0.02396201600000003, 0.279410174, 2.902791034,
                                            41.546003195]
varying_size_duration_point_distance = [0.011282185999999972, 0.09882280099999996, 0.9747950499999999, 9.510249106,
                                        96.42749661799999]
plt.plot(sizes, varying_size_duration_necklace_splitting, label='Necklace-Splitting')
plt.plot(sizes, varying_size_duration_point_distance, label='Point-Distance')
plt.xlabel("Size")
plt.ylabel("Time (sec)")
plt.xticks(sizes)
plt.xscale('log')
plt.title('Varying dataset size vs. preprocessing time (ratio=0.1, number of buckets=100)')
plt.legend(loc="upper left")
plt.savefig("plots/preprocessing_time_size.png")
plt.close()

varying_ratio_duration_necklace_splitting = [2.8017468490000397, 3.9884632760000045, 3.3253831940000396,
                                             2.2246699519999993, 2.9243033660000037]
varying_ratio_duration_point_distance = [10.417404775000008, 9.88619672499999, 10.333877605999987, 9.924032949999997,
                                         9.616681303999997]
plt.plot(ratios, varying_ratio_duration_necklace_splitting, label='Necklace-Splitting')
plt.plot(ratios, varying_ratio_duration_point_distance, label='Point-Distance')
plt.xlabel("Minority Ratio")
plt.ylabel("Time (sec)")
plt.xticks(ratios)
plt.title('Varying minority ratio vs. preprocessing time (size=1000000, number of buckets=100)')
plt.legend(loc="best")
plt.savefig("plots/preprocessing_time_ratio.png")
plt.close()

varying_num_of_buckets_duration_necklace_splitting = [1.7965001379999999, 2.8215191539999998, 8.473059483,
                                                      37.50363046300001, 168.665816876]
varying_num_of_buckets_duration_point_distance = [9.87145957300001, 9.635977951000001, 9.952218903000016,
                                                  10.665916978000013, 9.941547191000012]
plt.plot(num_of_buckets, varying_num_of_buckets_duration_necklace_splitting, label='Necklace-Splitting')
plt.plot(num_of_buckets, varying_num_of_buckets_duration_point_distance, label='Point-Distance')
plt.xlabel("Number of Buckets")
plt.ylabel("Time (sec)")
plt.xticks(num_of_buckets)
plt.xscale('log')
plt.title('Varying number of buckets vs. preprocessing time (ratio=0.1, size=1000000)')
plt.legend(loc="upper left")
plt.savefig("plots/preprocessing_time_bucket.png")
plt.close()

varying_size_space_point_distance = [239, 1088, 6261, 18271, 77223]
varying_size_space_necklace_splitting = [313, 366, 388, 397, 398]
varying_size_space_necklace_splitting_ = [x // 2 for x in varying_size_space_necklace_splitting]
# plt.plot(sizes, varying_size_space_necklace_splitting, label='Necklace-Splitting')
plt.plot(sizes, varying_size_space_necklace_splitting_, label='Necklace-Splitting')
plt.plot(sizes, varying_size_space_point_distance, label='Point-Distance')

plt.xlabel("Size")
plt.ylabel("Space")
plt.xticks(sizes)
plt.xscale('log')
plt.yscale('log')
plt.title('Varying dataset size vs. space (ratio=0.1, number of buckets=100)')
plt.legend(loc="upper left")
plt.savefig("plots/space_size.png")
plt.close()

varying_ratio_space_point_distance = [18271, 24387, 33745, 25303, 25869]
varying_ratio_space_necklace_splitting = [397, 398, 398, 396, 398]
varying_ratio_space_necklace_splitting_ = [x // 2 for x in varying_ratio_space_necklace_splitting]
# plt.plot(ratios, varying_ratio_space_necklace_splitting, label='Necklace-Splitting')
plt.plot(ratios, varying_ratio_space_necklace_splitting_, label='Necklace-Splitting')
plt.plot(ratios, varying_ratio_space_point_distance, label='Point-Distance')
plt.xlabel("Minority Ratio")
plt.ylabel("Space")
plt.xticks(ratios)
plt.yscale('log')
plt.title('Varying minority ratio vs. space (size=1000000, number of buckets=100)')
plt.legend(loc="best")
plt.savefig("plots/space_ratio.png")
plt.close()

varying_num_of_buckets_space_point_distance = [1899, 18271, 125773, 182781, 279239]
varying_num_of_buckets_space_necklace_splitting = [38, 397, 3962, 38297, 380000]  # estimate, fix later
varying_num_of_buckets_space_necklace_splitting_ = [x // 2 for x in varying_num_of_buckets_space_necklace_splitting]
# plt.plot(num_of_buckets, varying_num_of_buckets_space_necklace_splitting, label='Necklace-Splitting')
plt.plot(num_of_buckets, varying_num_of_buckets_space_necklace_splitting_, label='Necklace-Splitting')
plt.plot(num_of_buckets, varying_num_of_buckets_space_point_distance, label='Point-Distance')
plt.xlabel("Number of Buckets")
plt.ylabel("Space")
plt.xscale('log')
plt.yscale('log')
plt.xticks(num_of_buckets)
plt.title('Varying number of buckets vs. space (ratio=0.1, size=1000000)')
plt.legend(loc="upper left")
plt.savefig("plots/space_bucket.png")
plt.close()

varying_size_query_time_necklace_splitting = [6.727400000011708e-07, 1.049650000000124e-06, 8.081099999790454e-07,
                                              9.013799999735284e-07, 1.084329998661815e-06]
varying_size_query_time_point_distance = [7.104000000007771e-07, 8.985599999983273e-07, 1.459809999997397e-06,
                                          1.7357999999134677e-06, 2.503589999065525e-06]
plt.plot(sizes, varying_size_query_time_necklace_splitting, label='Necklace-Splitting')
plt.plot(sizes, varying_size_query_time_point_distance, label='Point-Distance')
plt.xlabel("Size")
plt.ylabel("Time (sec)")
plt.xticks(sizes)
plt.xscale('log')
plt.title('Varying dataset size vs. query time (ratio=0.1, number of buckets=100)')
plt.legend(loc="upper left")
plt.savefig("plots/query_time_size.png")
plt.close()

varying_ratio_query_time_necklace_splitting = [1.4566400039939253e-06, 9.704700033807968e-07, 8.99759998560512e-07,
                                               9.718499978816907e-07, 1.0134700011121821e-06]
varying_ratio_query_time_point_distance = [1.7349100001418094e-06, 1.813579999918602e-06, 1.9563599998306813e-06,
                                           2.074189999348164e-06, 1.800469999935217e-06]
plt.plot(ratios, varying_ratio_query_time_necklace_splitting, label='Necklace-Splitting')
plt.plot(ratios, varying_ratio_query_time_point_distance, label='Point-Distance')
plt.xlabel("Minority Ratio")
plt.ylabel("Time (sec)")
plt.xticks(ratios)
plt.title('Varying minority ratio vs. query time (size=1000000, number of buckets=100)')
plt.legend(loc="best")
plt.savefig("plots/query_time_ratio.png")
plt.close()

varying_num_of_buckets_query_time_necklace_splitting = [6.679400000297874e-07, 9.719199998414751e-07,
                                                        1.5318500010153003e-06, 1.9853499952660057e-06,
                                                        2.2840100000032225e-06]  # estimate, fix later
varying_num_of_buckets_query_time_point_distance = [3.035200001022531e-06, 4.478999998980271e-06,
                                                    6.7470000004732356e-06, 7.201199998974062e-06,
                                                    1.992560000019239e-05]
plt.plot(num_of_buckets, varying_num_of_buckets_query_time_necklace_splitting, label='Necklace-Splitting')
plt.plot(num_of_buckets, varying_num_of_buckets_query_time_point_distance, label='Point-Distance')
plt.xlabel("Number of Buckets")
plt.ylabel("Time (sec)")
plt.xscale('log')
plt.xticks(num_of_buckets)
plt.title('Varying number of buckets vs. query time (ratio=0.1, size=1000000)')
plt.legend(loc="upper left")
plt.savefig("plots/query_time_bucket.png")
plt.close()
