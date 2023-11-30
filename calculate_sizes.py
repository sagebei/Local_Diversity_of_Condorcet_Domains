from cdl import *
import argparse
import pickle
from utils import get_unprocessed_filepath
from collections import Counter
import shutil
from collections import OrderedDict
from pathlib import Path


def calculate_size(cd, filepath, trs_score_size_folder_path):
    trs_score_size_list = []
    with filepath.open("rb") as f:
        state_score_list = pickle.load(f)
        for state, score in state_score_list:
            trs = cd.state_to_trs(state)
            size = cd.size(trs)
            trs_score_size_list.append((trs, score, size))

    trs_score_size_filepath = trs_score_size_folder_path / filepath.stem
    trs_score_size_filepath = trs_score_size_filepath.with_suffix(".pkl")
    with trs_score_size_filepath.open("wb") as f:
        pickle.dump(trs_score_size_list, f)

    # remove the file that has been processed.
    filepath.unlink()


parser = argparse.ArgumentParser(description="get the result",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-folder_path", type=Path, default="./results/6/14_0_100000_10_10_20_False_1N3_2N3")
args = parser.parse_args()
config = vars(args)
print(config)

folder_path = config['folder_path']

n = int(folder_path.parent.name)
cd = CondorcetDomain(n)
num_triples = cd.num_triples

trs_score_size_folder_path = folder_path / f"trs_score_size"
trs_score_size_folder_path.mkdir(parents=True, exist_ok=True)
sub_folder_path = folder_path / f"{cd.num_triples}_{cd.num_triples}/"

filepath = get_unprocessed_filepath(sub_folder_path)
while filepath.stem != "none":
    # try:
    filepath = filepath.rename(filepath.with_suffix(".processing"))
    print(filepath)
    calculate_size(cd, filepath, trs_score_size_folder_path)
    # except Exception as e:
    #     print(e)

    filepath = get_unprocessed_filepath(sub_folder_path)


if len(list(sub_folder_path.iterdir())) == 0:
    # build and save the size counter
    sizes = []
    for trs_score_size_filepath in trs_score_size_folder_path.iterdir():
        with trs_score_size_filepath.open("rb") as f:
            trs_score_size_list = pickle.load(f)
            sizes.extend([size for _, _, size in trs_score_size_list])

    counter_filepath = folder_path / "counter.txt"
    with counter_filepath.open("w") as f:
        result = Counter(sizes)
        result = OrderedDict(sorted(result.items(), key=lambda t: t[0]))
        f.write(str(result))

    # remove unused folders
    for i in range(num_triples + 1):
        shutil.rmtree(folder_path / f"/{i}_{num_triples}", ignore_errors=True)




