#!/bin/sh

id0=$(sbatch ./skip.sh 2)
id0=${id0##* }
id0=$(sbatch --dependency=afterok:$id0 ./aggregate.sh)
