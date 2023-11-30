import argparse
import pickle
import os
from cdl import *
from pathlib import Path


parser = argparse.ArgumentParser(description="filter schemes in parallel",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-n_from", type=int, default=7)
parser.add_argument("-n_to", type=int, default=8)
parser.add_argument("-cutoffs_from", nargs="*", type=int, default=[40])
parser.add_argument("-cutoff_to", type=int, default=40)
parser.add_argument("-text_domains", type=Path, default="./domain_files")
parser.add_argument("-result_path", type=Path, default="./")
args = parser.parse_args()
config = vars(args)
print(config)

trs_path = f"{config['result_path']}/trs/{config['n_to']}_{config['cutoffs_from']}_{config['cutoff_to']}"
if not os.path.exists(trs_path):
    os.makedirs(trs_path)


cd_from = CondorcetDomain(config['n_from'])
cd_to = CondorcetDomain(config['n_to'])

trs_id = 1
domain_folder = f"{config['text_domains']}/{config['n_from']}"
for filename in os.listdir(domain_folder):
    cutoff_value = int(filename.split("=")[-1])
    if cutoff_value in config["cutoffs_from"]:
        with open(f"{domain_folder}/{filename}", "r") as f:
            domains = []
            content = f.read()
            domain = []
            for line in content.split('\n'):
                if line == '-1':
                    domains.append(domain)
                    domain = []
                else:
                    domain.append([int(i) for i in line.split()])

            for domain in domains:
                trs_from = cd_from.domain_to_trs(domain)
                trs_to = cd_to.init_trs()
                for tr in trs_from:
                    trs_to = cd_to.assign_id(trs_to, tr.triple, tr.rule_id)
                    state_to = cd_to.trs_to_state(trs_to)
                with open(f"{trs_path}/{cutoff_value}_{trs_id}.pkl", "wb") as f:
                    pickle.dump([(state_to, 0)], f)

                trs_id += 1


