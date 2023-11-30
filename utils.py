import pickle
from collections import Counter
import os
from collections import OrderedDict, defaultdict
from cdl import *
import random


class StaticFeature:
    def __init__(self, cd):
        self.cd = cd
        self.cd.init_trs()
        self.cd.init_subset(6)
        self.sub_cd = CondorcetDomain(6)

    def score_function(self, trs, cutoff, threshold):
        domain = self.cd.domain(trs)
        sub_domain_list = self.cd.subset_domain_list(domain)
        for sub_domain in sub_domain_list:
            if len(sub_domain) < cutoff:
                return -1
        return 0


class Search:
    def __init__(self, cd, rules, result_path):
        self.cd = cd
        self.sf = StaticFeature(cd)
        self.rules = rules
        self.result_path = result_path
        self.folder_path = result_path / str(cd.n)

    def expand_trs(self,
                   trs,
                   cutoff,
                   threshold):

        triple = self.cd.next_unassigned_triple(trs)
        trs_score_list = []
        for rule in self.rules:
            trs = self.cd.assign_rule(trs, triple, rule)
            score = self.sf.score_function(trs, cutoff, threshold)
            if score > -1:
                trs_score_list.append((trs, score))

        return trs_score_list

    def save_trs_score_list(self,
                            trs_list,
                            sub_folder_name,
                            filename):

        sub_folder_path = self.folder_path / sub_folder_name
        sub_folder_path.mkdir(parents=True, exist_ok=True)

        filepath = sub_folder_path / filename
        with filepath.open("wb") as f:
            trs_score_list = []
            for trs, score in trs_list:
                state = self.cd.trs_to_state(trs)
                trs_score_list.append((state, score))
            pickle.dump(trs_score_list, f)

    def load_trs_score_list(self,
                            sub_folder_path,
                            filename):

        filepath = sub_folder_path / filename
        with filepath.open("rb") as f:
            state_score_list = pickle.load(f)

        trs_score_list = []
        for state, score in state_score_list:
            trs = self.cd.state_to_trs(state)
            trs_score_list.append((trs, score))
        return trs_score_list

    def get_size_counter(self):

        sizes = []
        trs_score_size_list = []
        sub_folder_path = self.folder_path / f"{self.cd.num_triples}_{self.cd.num_triples}"
        for filename in sub_folder_path.iterdir():
            trs_score_list = self.load_trs_score_list(sub_folder_path, filename)
            for trs, score in trs_score_list:
                size = self.cd.size(trs)
                sizes.append(size)
                trs_score_size_list.append((trs, score, size))

        result = Counter(sizes)
        result = OrderedDict(sorted(result.items(), key=lambda t: t[0]))

        with open(f"{self.folder_path}/trs_score_size.pkl", "wb") as f:
            pickle.dump(trs_score_size_list, f)

        return result


def get_unprocessed_filepath(sub_folder_path, buffer_size=10000):
    counter = 0
    unprocessed_filepaths = []
    for filepath in sub_folder_path.iterdir():
        if filepath.suffix == ".pkl":
            unprocessed_filepaths.append(filepath)
            counter += 1

        if counter == buffer_size:
            break

    if len(unprocessed_filepaths) == 0:
        return sub_folder_path / "none.pkl"

    return random.choice(unprocessed_filepaths)


