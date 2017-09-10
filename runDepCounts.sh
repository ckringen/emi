#!/bin/bash

#SBATCH --mem=128G
#SBATCH -t 5-0:00

param=$1
out_path=/om/user/ckringen/parsing
data=profiling/SampleData/sample_dep_parses.txt.gz  #/om/user/ckringen/parsing/en.00.parsed.aa

counted_path=$out_path/$param-counted.gz
sorted_path=$out_path/$param-sorted.gz
summed_path=$out_path/$param.xz

countscript=./src/dependency_parsing/parse_dep_output.py
uniqsum_script=./src/uniqsum.sh

time zcat $data | python $countscript | gzip > $counted_path

# this isn't quite working...
#time ~/gz-sort/gz-sort -S 128G $counted_path $sorted_path
time zcat $counted_path | sort | uniq | gzip > $sorted_path

time gzip -dc $sorted_path | $uniqsum_script | xz > $summed_path


