#!/bin/sh
#SBATCH --mem=128G
#SBATCH -t 5-0:00
# a var #SBATCH --array=0-2

# run from root
# Count skip-grams from common crawl files.
# Parameters: num: just use as an identifier, e.g. "coroutines_en20.partaa"
#             degree: skipgram degree. 0 is normal bigrams.

num=$1
degree=$2
data=/om/user/ckringen/data/commoncrawl_en_deduped_filtered/en.10.gz
#${SLURM_ARRAY_TASK_ID}.gz

counted_path=/om/user/ckringen/en.$num-bigrams-$degree-counted.gz
sorted_path=/om/user/ckringen/en.$num-bigrams-$degree-sorted.gz
summed_path=/om/user/ckringen/en.$num-bigrams-$degree.xz

count_script=cpp/count_skipgrams 
uniqsum_script=./src/uniqsum.sh

#time zcat $data | python ./src/$count_script $data $degree | gzip > $counted_path

time zcat $data | ./src/$count_script $data $degree | gzip > $counted_path

# pushd ./prepro
# time xzcat $data | 
#   ./prepro_post_dedupe.sh en | 
#   ./prepro_tokenize.sh en truecasemodels/truecase-model.en | 
#   python ../$count_script $degree $size | gzip > $counted_path
# popd
  
time /om/user/ckringen/thirdparty/gz-sort/gz-sort -S 128G $counted_path $sorted_path

time gzip -dc $sorted_path | $uniqsum_script | xz > $summed_path
