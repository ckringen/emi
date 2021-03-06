#!/bin/sh
#SBATCH --mem=256G
#SBATCH -t 5-0:00

identifier=$1
degree=$2
user=`whoami`
out_path=/om/user/$user/en.$degree-grams-$identifier-counted.gz

# # clean and make
# make clean && \
#     make thread

# # run
# if [ -f main_thread ] 
# then
#     echo running program $out_path
#     #time ./main_thread $degree | gzip > $out_path
#     time ./dep $degree | gzip > $out_path
# fi

time ./dep $degree | gzip > $out_path

