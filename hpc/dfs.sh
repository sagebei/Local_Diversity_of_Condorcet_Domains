#!/bin/bash

#$ -cwd
#$ -pe smp 1
#$ -l h_vmem=8G
#$ -j y
#$ -l h_rt=240:0:0
#$ -t 1-1000
#$ -N udp

module load python/3.8.5
module load gcc/12.1.0

source ~/venv/bin/activate

python ~/CondorcetProjects/uplift_domains/dfs.py -n $1  \
                                                 -cutoffs_from $2 \
                                                 -cutoff_to $2 \
                                                 -chunk_size 10000 \
                                                 -rules "2N1" "2N3" "1N2" "3N2" "1N3" "3N1" \
                                                 -result_path "/data/scratch/acw554/uplift_domains" \




