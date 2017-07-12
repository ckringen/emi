
# profile source code functions

import sys
import random
import itertools
from collections import Counter

from src import count_skipgrams as skip
from CPerf import CPerf

    
# --------------------------------------------------- #
#            benchmarking functions                   #
# --------------------------------------------------- #    
# def bench_ichunks( self ):
#     skip.ichunks( self.s, 3 )

    
# def bench_tee( self ):
#     its = itertools.tee(xs, window_size)
#     for i, iterator in enumerate(its):
#         for _ in range(i):
#             next(iterator)

#@cPerf
def bench_tokenizeSmallString(  ):
    s = "dog's running real fast, I tell you hwat"
    skip.tokenize( s )
    

#@cPerf
def bench_flat(  ):
    lst = [['a','b'],'c',['d'], [['e','f'],['g'],['h']],'i',[[[[[['j']]]]]]]
    itertools.chain.from_iterable( lst )

    
# def bench_from_iterable( self ):
#     grams = flat(map(get_skipgrams, map(tokenize, lines)))

    
# def bench_get_skipgrams( self ):
#     skip.get_skipgrams( )

    
# def bench_map_get_skipgrams( self ):
#     skip.map(get_skipgrams, map(tokenize, lines))

    
# def bench_CounterUnigrams( self, long_string ):
#     Counter(long_string)

    
# def bench_CounterNgrams( self ):

    
# def bench_CounterSkipgrams( self ):

        
@CPerf
def bench_count_skipgrams_main(  ):
    ''' benchmark the whole file '''
    text = "Here Here is is is a a a a is a is a fairly good good fairly example of example of a piece of text of text."
    skip.main2( 2, text, 100000 )


        
if __name__ == "__main__":
        
    if len(sys.argv) > 1:

        outfile = sys.argv[2]
        CPerf.runAll( outfile )
        
    else:
        print("missing profiler, outfile, and function parameters")
