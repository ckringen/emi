#!/bin/sh
#SBATCH --mem=128G
#SBATCH -t 5-0:00

path=/om/user/ckringen
path_full=/om/user/ckringen/*                    #  kleene star keeps full file paths, recursively grabs subdirs
xzs=`ls $path_full | grep -P "en\.\d\d-bigrams-\d-counted\.txt\.gz"`
uniqsum_script=/home/ckringen/emi/src/uniqsum.sh

echo "aggregating"   $xzs
time zcat $xzs | gzip > /om/user/ckringen/full_en.txt.gz

echo "sorting"
time /home/ckringen/gz-sort/gz-sort -S 256G $path/full_en.txt.gz $path/full_en-sorted.txt.gz

echo "uniq sum ing"
time gzip -dc $path/full_en-sorted.txt.gz | $uniqsum_script | xz > $path/full_en.txt.xz
