#!/bin/sh
#SBATCH --mem=128G
#SBATCH -t 5-0:00
#SBATCH --array=0-94

# skipgram distance, e.g. the "3" in 2-skip-3-gram, assuming "2 skip" for all project
degree=$1

# if slurm array task id is a single digit, need to append a zero
if (( ${SLURM_ARRAY_TASK_ID} < 10 ))
then
    id=0${SLURM_ARRAY_TASK_ID}
else 
    id=${SLURM_ARRAY_TASK_ID}
fi

#data=/om/user/ckringen/data/commoncrawl_en_deduped_filtered/en.$id.gz
files=(/om/user/ckringen/data/parsing2/*)
pydata="${files[${SLURM_ARRAY_TASK_ID}]}"
counted_path=/om/user/ckringen/en.$id-bigrams-$degree-counted.txt.gz

#cpp/count_skipgrams 
count_script=python/dependency_parsing/parse_dep_output.py 

echo "counting the skipgrams " $pydata   $counted_path
time zcat $pydata | python ./$count_script | gzip > $counted_path
#time zcat $data | ./$count_script $data $degree | gzip > $counted_path

