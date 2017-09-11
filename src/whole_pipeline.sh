#!/bin/sh

id0=$(sbatch --qos=cpl ./src/countsortmerge2.sh)
id0=${id0##* }
id0=$(sbatch --qos=cpl --dependency=afterok:$id0 ./src/aggregate.sh)
