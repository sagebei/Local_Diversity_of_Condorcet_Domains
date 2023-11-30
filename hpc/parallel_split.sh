#!/bin/bash

#$ -cwd
#$ -pe smp 1
#$ -l h_vmem=8G
#$ -j y
#$ -l h_rt=240:0:0
#$ -t 1-1000
#$ -N ps

module load python/3.8.5
module load gcc/12.1.0

source ~/venv/bin/activate

python ~/CondorcetProjects/uplift_domains/parallel_split.py -n $1  \
                                                            -cutoff $2 \
                                                            -threshold $2 \
                                                            -split_depth 5 \
                                                            -n_chunks 10000 \
                                                            -shuffle "" \
                                                            -rules "2N1" "2N3" "1N2" "3N2" "1N3" "3N1" \
                                                            -result_path "/data/scratch/acw554/uplift_domains/trs/8_[40]_40" \




