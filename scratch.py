from ranking_2d import find_fair_ranking

num_of_buckets = 10
(
    disparity,
    disparity_original,
    # distribution,
    ranking,
    theta,
    duration,
) = find_fair_ranking("real_data/dummy.csv", ["fnlwgt", "fnlwgt_"], "sex", 10)
