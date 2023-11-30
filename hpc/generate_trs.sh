#!/bin/bash

#$ -cwd
#$ -j y
#$ -pe smp 1            # Request cores (8 per GPU)
#$ -l h_vmem=8G         # 11G RAM per core
#$ -l h_rt=1:0:0      # Max 1hr runtime (can request up to 240hr)
#$ -N upc

module load python/3.8.5
module load gcc/12.1.0

source ~/venv/bin/activate

python ~/CondorcetProjects/uplift_domains/generate_trs.py -n_from $1 \
                                                          -n_to $2  \
                                                          -cutoffs_from $3 \
                                                          -cutoff_to $3 \
                                                          -text_domains "/data/home/acw554/CondorcetProjects/uplift_domains/domain_files" \
                                                          -result_path "/data/scratch/acw554/uplift_domains"
