
# profile source code functions

import sys

from memory_profiler import profile
import line_profiler

from src import count_skipgrams as skip


class conditional_decorator(object):
    def __init__(self, dec, condition):
        self.decorator = dec
        self.condition = condition

    def __call__(self, func):
        if not self.condition:
            return func
        return self.decorator(func)


def cond_dec( func, cflag ):
    if not cflag:
        return func
    else:
        def wrapper(*args, **kwargs):
            return func
        return wrapper
        

class perf( ):

    def __init__(self):
        pass    
    
    def setUp(self):
        pass

    def bench_tokenizeSmallString( self ):
        s = "the dog ran quickly across the field"
        skip.tokenize( s )

    def bench_ichunks( self ):
        s = "the dog ran quickly across the field"
        skip.ichunks( s, 3 )
        
        
    # @profile
    # def bench_tee( self ):

        
    def tearDown(self):
        pass



if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "1":
            p = perf( )
            p.bench_tokenizeSmallString = profile(p.bench_tokenizeSmallString)
            p.bench_tokenizeSmallString( )
            
        if sys.argv[1] == "2":
            p = perf( )
            profile = line_profiler.LineProfiler( p.bench_tokenizeSmallString )
            profile.enable( )
            p.bench_tokenizeSmallString( )
            profile.print_stats()
            
        if sys.argv[1] == "3":
            p = perf()
            p.bench_tokenizeSmallString( )

    
