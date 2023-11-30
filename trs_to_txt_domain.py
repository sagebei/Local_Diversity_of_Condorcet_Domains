from cdl import *
import argparse
import pickle
import os
from collections import OrderedDict, Counter


parser = argparse.ArgumentParser(description="get the result",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-folder_path", type=str, default="./8/0_10000_2N1_2N3_1N2_3N2_1N3_3N1/")
parser.add_argument("-text_domains", type=str, default="./domain_files")
args = parser.parse_args()
config = vars(args)
print(config)

folder_path = config['folder_path']

folders = folder_path.split("/")
if folders[-1] == "":
    folders = folders[:-1]
folder_path = "/".join(folders)
text_domains_path = config["text_domains"]

n = int(folders[-2])
cd = CondorcetDomain(n)
num_triples = cd.num_triples

sub_folder_path = f"{folder_path}/trs_score_size/"

if not os.path.exists(f"{text_domains_path}/{cd.n}"):
    os.makedirs(f"{text_domains_path}/{cd.n}")

print(sub_folder_path)

cutoff_values = set()
for filename in os.listdir(sub_folder_path):
    cutoff_values.add(filename.split('_')[0])

for cutoff in cutoff_values:
    domains = []

    for filename in os.listdir(sub_folder_path):
        if filename.split('_')[0] == cutoff:
            file = sub_folder_path + filename

            with open(file, "rb") as f:
                trs_score_size = pickle.load(f)

            for trs, _, _ in trs_score_size:
                domains.append(cd.domain(trs))

    domains = cd.non_isomorphic_domains(domains)
    sizes = []
    for domain in domains:
        size = len(domain)
        if size >= 0:
            sizes.append(size)
            with open(f"{text_domains_path}/{cd.n}/cds-n={cd.n}-ab={cutoff}", "a") as f:
                for d in domain:
                    permutation = " ".join([str(i) for i in d])
                    f.write(permutation + "\n")
                f.write("-1\n")

    counter = OrderedDict(sorted(Counter(sizes).items(), key=lambda t: t[0]))
    print(f"(6, {cutoff})-abundance : ", counter)








