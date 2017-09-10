#!/bin/sh

id0=$(sbatch ./src/countsortmerge2.sh)
id0=${id0##* }
id0=$(sbatch --dependency=afterok:$id0 ./src/aggregate.sh)
