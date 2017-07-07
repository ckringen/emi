#!/bin/bash

PROF=profiling

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
output_file=""

function show_help( ) {
    echo "options:
-c         : use the cProfile module
-l         : use the line_profiler module
-m         : use the memory_profiler module
-h         : show the help menu
-o         : name the output file
"
    }

while getopts "h?lmco:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    l)  pushd $PROF; python main.py 2; popd
	# pushd $PROF; kernprof -l main.py; python -m line_profiler main.py.lprof; popd
        ;;
    m)  pushd $PROF; python main.py 1; popd
	#pushd $PROF; python -m memory_profiler main.py; popd
        ;;
    c)  pushd $PROF; python -m cProfile main.py; popd
	;;
    o) output_file=$OPTARG
       ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift
