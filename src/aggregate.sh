#!/bin/sh

path=/om/user/ckringen/*
xzs=`ls $path | grep counted`
uniqsum_script=/home/ckringen/src/uniqsum.sh

echo "aggregating"   $xzs
# time zcat $path/$xzs > $path/full_en.gz

# echo "sorting"
# time /home/ckringen/gz-sort/gz-sort -S 256G $path/full_en.gz $path/full_en-sorted.gz

# echo "uniq sum ing"
# time gzip -dc $path/full_en-sorted.gz | $uniqsum_script | xz > $path/full_en.xz
