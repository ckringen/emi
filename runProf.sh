#!/bin/bash

# sample run:
# ./runProf.sh "-c bench_read_mmap bench_read_binary -t bench_read_stdin"
# outfiles look like "20170719_bench_read_mmap.tperf"

args=("$@")                     # yields all commandline args, provided they're quoted 

if [ ! -d "ProfileReports" ]; then
    echo "creating ProfileReports directory"
    mkdir ProfileReports
fi

python profiling/main.py $args

reports=`ls | grep -P "\.[c|t|l|m]perf"`

# -z checks if a variable is unset or equal to the empty string
if [ ! -z "$reports" ]; then
    mv $reports ProfileReports/
fi




