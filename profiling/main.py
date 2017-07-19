
# import benchmarks and modify select benchmark functions
# with appropriate performance decorators, e.g. "bench_read_mmap = CPerf(bench_read_mmap)"

import sys
import datetime

from ArgParser import parseCommandLine
import hook        # redefines import func, so either use it last or, figure out how to do "from lib import func" with it

if __name__ == "__main__":

    args = parseCommandLine( )
    
    bench = hook.custom_import( "benchmark_test",  args )   # decorates functions in benchmark

    b = bench.benchmark( args[1] )                              # adds functions to benchmark's global state
    b.runAll( ) 
    
