
# decorator cass, wrapper around simple timing via the 3rd party line-profiler

import line_profiler

class LPerf( ):
    ''' 
    global state object to hold all benchmark functions, plus some utility
    methods for running and formatting according to line by line profiling
    '''    

    lp = line_profiler.LineProfiler( )
    
    def __init__(self, function, out="logging.out"):
        ''' registers a function in the overall state object '''
        self.func = function
        LPerf.lp.add_function(function)

    def __call__( self, *args ):
        ''' instance of class getting called triggers this, i.e. a decorated function '''
        #lp = line_profiler.LineProfiler( self.func )
        LPerf.lp.enable_by_count( )
        self.func( self )
        LPerf.lp.disable_by_count( )        

        outf = self.getFilestream(*args)
        LPerf.lp.print_stats( stream = outf )
        
    def getFilestream( self, output):
        f = open(output,"w")
        return f
            

