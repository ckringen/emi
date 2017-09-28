#!/bin/sh
#SBATCH --mem=256G
#SBATCH -t 5-0:00

identifier=$1
degree=$2
out_path=/om/user/ckringen/en.$degree-grams-$identifier-counted.gz

#time python ./mpsc.py $degree | gzip > $out_path
time python ./dependency_parsing/mpsc_dependency.py #> $out_path
