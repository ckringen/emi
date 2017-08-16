
# decorator cass, wrapper around simple timing via the time module

# TODO:
# fix the printer method, nothing really to print at the moment

import functools
import time



class TPerf( ):
    ''' global state object to hold all benchmark functions, plus some utility
        methods for running and formatting according to time
    '''    
    def __init__(self, function, out="logging.out"):
        ''' registers a function in the overall state object '''
        self.func = function

    def __call__( self, obj, *args ):
        ''' instance of class getting called triggers this, i.e. a decorated function '''
        print("running self.func ", self.func)
        print(obj)
        
        a = time.time( )
        self.func( self )
        b = time.time ( )
        elapsed =  b - a 
        self.printCSVInstance(elapsed, obj )

    def __get__(self, obj, objtype):
        """Support instance methods."""
        print("getting called")
        return functools.partial(self.__call__, obj)

    def printCSVInstance( self, output, outfile ):
        with open( outfile, "w" ) as f:
            output = "elapsed time was: " + str(output)
            f.write(output)

            
