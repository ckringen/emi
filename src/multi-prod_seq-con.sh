#!/bin/sh
#SBATCH --mem=256G
#SBATCH -t 5-0:00

# to be run from emi/src.  can all be cleaned up later

identifier=$1
degree=$2
out_path=/om/user/ckringen/en.$degree-grams-$identifier-counted.gz

# # clean and make
# pushd cpp
# make clean && \
#     make thread
# popd cpp

# run
if [ -f cpp/main_thread ] 
then
    echo running program
    time ./cpp/main_thread $degree | gzip > $out_path
fi
