#!/bin/bash

# run the appropiate benchmarking fixture with functions (possibly none) to be decorated

OPTIND=1           # POSIX variable : Reset in case getopts has been used previously in the shell.
benchmark_dir="profiling/fixtures"
fixture=""
funcs=""
output_dir="ProfileReports"

function show_help( ) {
    echo "
Run a benchmarking suite. Writes profiler reports to ProfileReports/ (default) in root. 

Sample run:
          
./runProf.sh -f fixtureAsync \"-c tokenizeAsync countAsync -t bigramAsync\"

Make sure you're putting all flags+args except -f in quotes.

options:
-f         : file containing functions to run, should be a class inheriting from the benchFixture class
-h         : show the help menu
-c         : use the cProfile module
-l         : use the line_profiler module
-t         : use the time profiler module
-m         : use the memory_profiler module
-o         : string to use as output directory name
"
}

# really needs to be revised
# "-$opt" refers to re-putting a dash infront of the optional argument...
while getopts "h?f:l:m:t:c:o:" opt; do
    case "$opt" in
	h|\?)
	    show_help
	    exit 0
	    ;;
	l)  funcs="$funcs -$opt $OPTARG"
	    ;;
	f)  fixture=$OPTARG
	    ;;
	m)  funcs="$funcs -$opt $OPTARG"
	    ;;
	c)  funcs="$funcs -$opt $OPTARG"
	    ;;
	t)  funcs="$funcs -$opt $OPTARG"
	    ;;
	o) output_dir=$OPTARG
	   ;;
    esac
done

shift $((OPTIND-1))
[ "$1" = "--" ] && shift

# run the benchmark fixture
if [ ! -d $output_dir ]; then
    echo "creating $output_dir directory"
    mkdir $output_dir
fi

if [ ! -z $fixture ]; then
    python $benchmark_dir/$fixture.py $funcs
fi

# grab the output files 
reports=`ls | grep -P "\.[C|T|L|M|D]Perf"`

if [ ! -z "$reports" ]; then
    mv $reports $output_dir/
fi


