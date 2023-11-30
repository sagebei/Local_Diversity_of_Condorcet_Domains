#!/bin/bash

#$ -cwd
#$ -pe smp 1
#$ -l h_vmem=8G
#$ -j y
#$ -l h_rt=1:0:0
#$ -t 1-10
#$ -N ups

module load python/3.8.5
module load gcc/12.1.0

source ~/venv/bin/activate

python ~/CondorcetProjects/1n3_2n3/calculate_sizes.py -folder_path $1 \

