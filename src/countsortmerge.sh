#!/bin/sh
#SBATCH --mem=128G
#SBATCH -t 5-0:00

# Count skip-grams from common crawl files.
# Parameters: num: which common crawl file to use (00 through 99)
#             degree: skipgram degree. 0 is normal bigrams.

num=$1
degree=$2

size=10000000
data=/om/user/futrell/commoncrawl_en_deduped/en.$num.xz
#data=/om/user/futrell/en_small.xz
counted_path=/om/user/futrell/en.$num-bigrams-$degree-counted.gz
sorted_path=/om/user/futrell/en.$num-bigrams-$degree-sorted.gz
summed_path=/om/user/futrell/en.$num-bigrams-$degree.xz

count_script=count_skipgrams.py
uniqsum_script=uniqsum.sh
#count_script=count_ngrams.py

echo $data

pushd ~/prepro
time xzcat $data | 
  ./prepro_post_dedupe.sh en | 
  ./prepro_tokenize.sh en truecasemodels/truecase-model.en | 
  python $count_script $degree $size | gzip > $counted_path
popd
echo "Counted."
  
time gz-sort -S 128G $counted_path $sorted_path
echo "Sorted."

time gzip -dc $sorted_path | $uniqsum_script | xz > $summed_path
echo "Summed."

# The combined below pipeline doesn't work because sort says can't execute
# compress program when run in sbatch. This appears to be some kind
# of low-level multithreading bug, so I have no idea how to fix it.

#gzip -dc $counted_path | 
#  env LC_ALL=C sort --compress-program=lzop | 
#  $uniqsum_script | 
#  xz > $summed_path

