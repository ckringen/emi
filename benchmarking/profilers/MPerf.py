
# wrapper around memory_profiler

from memory_profiler import profile

class MPerf( ):
    ''' 
    global state object to hold all benchmark functions, plus some utility
    methods for running and formatting according to memory usage
    '''    
    
    def __init__(self, function, out="logging.out"):
        ''' registers a function in the overall state object '''
        self.func = function

    def __call__( self, *args ):
        ''' instance of class getting called triggers this, i.e. a decorated function '''
        outf = self.getFilestream(*args)
        self.func = profile(self.func, stream=outf)

        self.func( self )

    def getFilestream( self, output_string ):
        f = open(output_string,"w")
        return f
