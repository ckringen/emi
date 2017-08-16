#!/bin/shsh

# so this should be a good old-fashioned map/reduce
# map skipgram functions over a text file to get a counts file
# reduce all the counts files into a single counts file

future=/om/user/futrell/commoncrawl_en_deduped/
jobs=`ls $future | grep part | wc`

# map
sbatch --array=0-$jobs -N1 tmp

# reduce
# Wait for entire job array to complete
sbatch --depend=afterany:123 my.job


