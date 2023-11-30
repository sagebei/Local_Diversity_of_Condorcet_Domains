#!/bin/bash

#$ -cwd
#$ -pe smp 1
#$ -l h_vmem=8G
#$ -j y
#$ -l h_rt=24:0:0
#$ -N upt

module load python/3.8.5
module load gcc/12.1.0

source ~/venv/bin/activate

python ~/CondorcetProjects/uplift_domain/trs_to_txt_domain.py -folder_path $1 \
                                                              -text_domains "/data/home/acw554/CondorcetProjects/uplift_domains/domain_files" \

