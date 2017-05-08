DATA_DIR=/om/user/futrell/commoncrawl_en_deduped
RESULT_DIR=/om/futrell/skipgrams
TEMP_DIR=/om/scratch/Sat/futrell

d=$1
a=$@
filenames="${a[@]:1}"

for filename in $filenames; do
    sbatch count_skipgrams_single_file.sh $d $DATA_DIR/$filename.xz $TEMP_DIR/$filename-$d.gz
done

#cat $filenames > $TEMP_DIR/together-$d.gz # todo figure out bash syntax issues here
#time gz-sort $TEMP_DIR/together-$d.gz $TEMP_DIR/together-sorted-$d.gz
#rm $TEMP_DIR/together-$d.gz
#time zcat $TEMP_DIR/together-sorted-$d.gz | python add_counts.py | xz > $RESULT_DIR/skipgrams_$d.xz
#rm $TEMP_DIR/together-sorted-$d.gz
