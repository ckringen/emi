#!/bin/sh
#SBATCH --mem=256G
#SBATCH -t 5-0:00

identifier=$1
degree=$2
user=`whoami`
out_path=/om/user/$user/en.$degree-grams-$identifier-counted.gz

time python ./mpsc_dependency.py
