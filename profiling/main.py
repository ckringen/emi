
# create benchmark class with set of functions to be profiled

from ArgParser import parseCommandLine    
from benchmark_test import benchmark

if __name__ == "__main__":

    args = parseCommandLine( )  
    
    b = benchmark( args )

    b.runAll( )


