
# decorator cass, wrapper around simple timing via the 3rd party line-profiler

import line_profiler

class LPerf( ):
    ''' 
    global state object to hold all benchmark functions, plus some utility
    methods for running and formatting according to line by line profiling
    '''    
    
    def __init__(self, function, out="logging.out"):
        ''' registers a function in the overall state object '''
        self.func = function

    def __call__( self, *args ):
        ''' instance of class getting called triggers this, i.e. a decorated function '''
        lp = line_profiler.LineProfiler( self.func )
        lp.enable_by_count( )
        self.func( )
        lp.disable_by_count( )        
        lp.print_stats( )
        
    def printCSVInstance( self, output, outfile ):
        with open( outfile, "w" ) as f:
            output = "elapsed time was: " + str(output)
            f.write(output)

            

