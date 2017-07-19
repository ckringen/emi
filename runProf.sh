#!/bin/bash

# sample run:
# ./runProf.sh -c bench_read_mmap bench_read_binary -t bench_read_stdin


# remove old profiles, recreate directory, run profilers, stick reports in new dir
if [ -d ProfileReports/ ]
   rm -rf ProfileReports/
fi

mkdir ProfileReports/

python profilers/main.py ...?

# reports look like "20170719_bench_read_mmap.tperf"
reports=`ls | grep -P "\.[c|t|l|m]perf"`

mv reports ProfileReports/



# -- largely taken care of by python's argparser -- # 

# PROF=profiling
# funcs=${1:-""}  # pass in a list of functions you'd like to profile, defaults to all
# # A POSIX variable
# OPTIND=1         # Reset in case getopts has been used previously in the shell.

# # Initialize our own variables:
# output_file=""

# function show_help( ) {
#     echo "options:
# -c         : use the cProfile module
# -l         : use the line_profiler module
# -m         : use the memory_profiler module
# -h         : show the help menu
# -o         : name the output file
# "
#     }
# while getopts "h?lmco:" opt; do
#     case "$opt" in
#     h|\?)
#         show_help
#         exit 0
#         ;;
#     l)  pushd $PROF; python main.py 2 $funcs; popd
#         ;;
#     m)  pushd $PROF; python main.py 1 $funcs; popd
#         ;;
#     c)  pushd $PROF; python main.py -c $funcs; popd
# 	;;
#     o) output_file=$OPTARG
#        ;;
#     esac
# done

# shift $((OPTIND-1))

# [ "$1" = "--" ] && shift
