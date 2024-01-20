# FairHash: A Fair and Memory/Time-efficient Hashmap

### Companion repository for the paper "FairHash: A Fair and Memory/Time-efficient Hashmap". 



## Publication(s) to cite:
TBD.



## Installation
- Clone the repo
- Create a virtual environment using e.g., venv or Conda
- Install any missing packages using e.g., pip or Conda
  - main packages are fairly standard (e.g., Pandas, NumPy, Matplotlib)

## Usage
The algorithms are implemented in `[algorithm-name].py`. You can familiarize yourself with the code by looking at the `[algorithm-name]_test.py`. Each algorithm accepts the following inputs:
- Dataset
- Sensitive attribute (categorical)
- Non-sensitive attributes (ordinal real-valued)
- Number of buckets
The algorithm returns a sorted list of boundaries that specify the boundaries for each hash bucket.

### Data for reproducing the results:
- The data used in our experiments can be downloaded from here: [Link]([https://drive.google.com/file/d/1vJztJVfEh3Rf5QpPBmmyTB55FIY9Z-Ci/view?usp=sharing](https://drive.google.com/file/d/1qG9NC_6HGRbmK3-gEYK-6XijJNfHPgMy/view?usp=sharing)) 

### Reproducing the results:
- Unzip the data folder in the root directory of the project
- The following Python files will reproduce the experiments for each algorithm:
  - Necklace Splitting algorithm results: `python necklace_split_binary_test.py`
  - Sweep & Cut algorithm results: `python sweep_and_cut_test.py`
  - Sampled Ranking algorithm results: `python ranking_sampled_vector_test.py`
  - Ranking (ray sweeping) algorithm results: `python ranking_2d_test.py`
  - Local Search heuristic results: `python local_search.py`
- Testing FairHash on held-out data: `python train_test.py`

## Notice
This project is still under development, so please beware of potential bugs, issues, etc. Use at your own responsibility in practice.

## Contact
TBD.
<!---Feel free to contact the authors or leave an issue in case of any complications. We will try to respond as soon as possible.-->

## License

This project is licensed under the MIT License &mdash; see the [LICENSE.md](LICENSE.md) file for details.

<!---<p align="center"><img width="20%" src="https://www.cs.uic.edu/~indexlab/imgs/InDeXLab2.gif"></p>-->

