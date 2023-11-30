import os
from cdl import *
from utils import Search
from utils import get_unprocessed_filepath
import argparse
import sys
from pathlib import Path
sys.setrecursionlimit(5000)


class ExhaustiveSearch(Search):
    def __init__(self, cd, rules, result_path):
        super().__init__(cd, rules, result_path)
        self.chunk_id = 1

    def fill_trs(self,
                 trs,
                 cutoff,
                 threshold,
                 full_trs_score_list,
                 chunk_size,
                 file_id):

        triple = self.cd.next_unassigned_triple(trs)
        if triple == [0, 0, 0]:
            score = self.sf.score_function(trs, cutoff, threshold)
            if score > -1:
                full_trs_score_list.append((trs, score))
                if len(full_trs_score_list) >= chunk_size:
                    self.save_trs_score_list(full_trs_score_list,
                                             f"{self.cd.num_triples}_{self.cd.num_triples}",
                                             f"{file_id}_{self.chunk_id}.pkl")
                    full_trs_score_list.clear()
                    self.chunk_id += 1
        else:
            for rule in self.rules:
                new_trs = self.cd.assign_rule(trs, triple, rule)
                score = self.sf.score_function(new_trs, cutoff, threshold)

                if score == -1:
                    continue
                else:
                    self.fill_trs(new_trs,
                                  cutoff,
                                  threshold,
                                  full_trs_score_list,
                                  chunk_size,
                                  file_id)

    def static_search(self,
                      cutoffs_from,
                      cutoff_to,
                      threshold,
                      chunk_size):

        folder_name = f"{threshold}_{chunk_size}_" + f"_".join(self.rules) + f"{cutoffs_from}" + f"{cutoff_to}"
        self.folder_path = self.folder_path / folder_name

        trs_path = self.result_path / "trs" / f"{self.cd.n}_{cutoffs_from}_{cutoff_to}"
        filepath = get_unprocessed_filepath(trs_path)
        while filepath.stem != "none":
            try:
                filepath = filepath.rename(filepath.with_suffix(".processing"))
                trs_score_list = self.load_trs_score_list(trs_path,
                                                          filepath.name)

                full_trs_score_list = []
                self.chunk_id = 1
                for trs, _ in trs_score_list:
                    self.fill_trs(trs,
                                  cutoff_to,
                                  threshold,
                                  full_trs_score_list,
                                  chunk_size,
                                  filepath.stem)

                if len(full_trs_score_list) > 0:
                    self.save_trs_score_list(full_trs_score_list,
                                             f"{self.cd.num_triples}_{self.cd.num_triples}",
                                             f"{filepath.stem}_{0}.pkl")

                filepath.unlink()

            except FileNotFoundError as e:
                print(e)

            filepath = get_unprocessed_filepath(trs_path)


parser = argparse.ArgumentParser(description="Run search on a single CPU core",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-n", type=int, default=8)
parser.add_argument("-rules", nargs="*", type=str, default=["2N1", "2N3"])
parser.add_argument("-cutoffs_from", nargs="*", type=int, default=[40])
parser.add_argument("-cutoff_to", type=int, default=40)
parser.add_argument("-threshold", type=float, default=0)
parser.add_argument("-result_path", type=Path, default="./")
parser.add_argument("-chunk_size", type=int, default=100000)
args = parser.parse_args()
config = vars(args)
print(config)

cd = CondorcetDomain(n=config['n'])
es = ExhaustiveSearch(cd, rules=config['rules'], result_path=config['result_path'])
es.static_search(cutoffs_from=config['cutoffs_from'],
                 cutoff_to=config['cutoff_to'],
                 threshold=config['threshold'],
                 chunk_size=config["chunk_size"])


# python parallel_search.py -n 6 -cutoff 16 -threshold 0 -top_n 1000 -rules "2N3" "2N1"  -triple_id 6 -core_id 2


