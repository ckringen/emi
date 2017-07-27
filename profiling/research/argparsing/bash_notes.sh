#!/bin/bash

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

fixture=""
funcs=""

function show_help( ) {
    echo "options:
-c         : use the cProfile module
-l         : use the line_profiler module
-m         : use the memory_profiler module
-h         : show the help menu
-o         : name the output file
-f         : fixture containing functions to run
"
}

while getopts "h?f:l:m:c:" opt; do
    case "$opt" in
	h|\?)
	    show_help
	    exit 0
	    ;;
	l)  funcs="$funcs $OPTARG"
	    ;;
	f)  fix=$OPTARG
	    ;;
	m)  funcs="$funcs $OPTARG"
	    ;;
	c)  funcs="$funcs $OPTARG"
	    ;;
	t)  funcs="$funcs $OPTARG"
	    ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

# run the benchmark fixture
if [ ! -d "ProfileReports" ]; then
    echo "creating ProfileReports directory"
    mkdir ProfileReports
fi

if [ ! -z $fixture ]; then
    python $fixture $funcs
fi

reports=`ls | grep -P "\.[C|T|L|M]Perf"`

if [ ! -z "$reports" ]; then
    mv $reports ProfileReports/
fi


