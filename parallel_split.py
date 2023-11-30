import random
from cdl import *
from utils import Search
from utils import get_unprocessed_filepath
import argparse
import numpy as np
import pickle
from pathlib import Path


class ExhaustiveSearch(Search):
    def __init__(self, cd, rules, result_path):
        super().__init__(cd, rules, result_path)

    def static_search(self,
                      cutoff=16,
                      threshold=0,
                      split_depth=5,
                      n_chunks=1000,
                      shuffle=False):

        filepath = get_unprocessed_filepath(self.result_path)  # trs\8_[40]_40\40_228.pkl
        tmp_folder = filepath.parent.parent / "tmp"
        tmp_folder.mkdir(parents=True, exist_ok=True)

        while filepath.stem != "none":
            try:
                filepath = filepath.rename(filepath.with_suffix(".processing"))
                trs_score_list = self.load_trs_score_list(self.result_path,
                                                          filepath.name)

                for i in range(split_depth):
                    next_trs_score_list = []
                    for trs, _ in trs_score_list:
                        trs_value_list = self.expand_trs(trs, cutoff, threshold)
                        next_trs_score_list.extend(trs_value_list)

                    trs_score_list.clear()
                    trs_score_list = next_trs_score_list

                if len(trs_score_list) > 0:
                    if shuffle:
                        random.shuffle(trs_score_list)
                    split_trs_score_list = np.array_split(np.array(trs_score_list, dtype=object),
                                                         min(n_chunks, len(trs_score_list)))

                    for i, t in enumerate(split_trs_score_list):
                        with open(tmp_folder / f"{filepath.stem}_{str(i)}.pkl", "wb") as f:
                            trs_score_list = []
                            for trs, score in t:
                                state = self.cd.trs_to_state(trs)
                                trs_score_list.append((state, score))
                            pickle.dump(trs_score_list, f)

                filepath.unlink()

            except FileNotFoundError as e:
                print(e)

            filepath = get_unprocessed_filepath(self.result_path)

        if len(list(self.result_path.iterdir())) == 0:
            tmp_folder.replace(self.result_path)


parser = argparse.ArgumentParser(description="Run search on a single CPU core",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-n", type=int, default=6)
parser.add_argument("-rules", nargs="*", type=str, default=["2N1", "2N3"])
parser.add_argument("-cutoff", type=int, default=16)
parser.add_argument("-threshold", type=float, default=0)
parser.add_argument("-split_depth", type=int, default=3)
parser.add_argument("-n_chunks", type=int, default=10)
parser.add_argument("-shuffle", type=bool, default="")
parser.add_argument("-result_path", type=Path, default="./trs/8_[40]_40/")
args = parser.parse_args()
config = vars(args)
print(config)

cd = CondorcetDomain(n=config['n'])
es = ExhaustiveSearch(cd, rules=config['rules'], result_path=config['result_path'])
es.static_search(cutoff=config['cutoff'],
                 threshold=config['threshold'],
                 split_depth=config['split_depth'],
                 n_chunks=config['n_chunks'],
                 shuffle=config['shuffle'])


# python parallel_search.py -n 6 -cutoff 16 -threshold 0 -top_n 1000 -rules "2N3" "2N1"  -triple_id 6 -core_id 2


