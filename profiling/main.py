
# profile source code functions

import sys, os
import random
import itertools
import fileinput
import mmap
from collections import Counter

from src import count_skipgrams as skip
from CPerf import CPerf
from TPerf import timer


# --------------------------------------------------- #
#            data processing pipeline                 #
# --------------------------------------------------- #    
@CPerf
def bench_ichunks( ):
    s = "dog's running real fast, I tell you hwat"
    skip.ichunks( s, 3 )


@CPerf
def bench_tee( self ):
    its = itertools.tee(xs, window_size)
    for i, iterator in enumerate(its):
        for _ in range(i):
            next(iterator)

            
@CPerf
def bench_tokenizeSmallString( ):
    s = "dog's running real fast, I tell you hwat"
    skip.tokenize( s )
    

@CPerf
def bench_islice( ):
    
    myiter = itertools.islice(sys.stdin, 100000)

    
@CPerf
def bench_flat( ):
    lst = [['a','b'],'c',['d'], [['e','f'],['g'],['h']],'i',[[[[[['j']]]]]]]
    itertools.chain.from_iterable( lst )

    
@CPerf
def bench_from_iterable( ):
    grams = flat(map(get_skipgrams, map(tokenize, lines)))

    
@CPerf
def bench_get_skipgrams( ):
    tokens = ['<s>', 'Here', 'Here', 'is', 'is', 'is', 'a', 'a', 'a', 'a', 'is', 'a', 'is', 'a', 'fairly', 'good', 'good', 'fairly', 'example', 'of', 'example', 'of', 'a', 'piece', 'of', 'text', 'of', 'text.', '</s>']
    gen = map(skip.get_skipgrams, tokens)



# --------------------------------------------------- #
#            reading data sources                     #
# --------------------------------------------------- #        
@timer
def bench_read_stdin( ):
    ''' read from sys.stdin by iter slice object, possible overhead in converting islice to list; this is done
    because to avoid an infinite loop wherein islice returns an iterator on an empty iterator the same it would on
    a nonempty iterator; https://stackoverflow.com/questions/44986908/yielding-islice-from-reading-file'''
    f = sys.stdin
    sentinel = object( )

    # choose whichever has less overhead
    # a.
    while True:
        it = list(itertools.islice(f, 1, 200 ))
        if not it:
            break

    # b.
    # while True:
    #     it = itertools.islice(f, 1, 200 )
    #     print([i for i in it])
    #     if next(it,sentinel) is sentinel:
    #         break

    
@timer
def bench_read_file( ):
    ''' read from file by iter slice object; suffers from same problem as above '''
    f = fileinput.input(files=("samples/large_file.txt"))
    while True:
        it = list(itertools.islice(f, 100000 ))
        if not it:
            break
    
    
@timer
def bench_read_bytes( ):
    ''' read from file by bytes '''
    with open("samples/large_file.txt") as f:
        while True:
            buf = f.read(100000)
            if not buf:
                break

    
@timer
def bench_read_mmap( mmap_file ):
    ''' read from memory-mapped file by bytes, assuming islice-size and buffer-size are the same '''

    buffer_size = 100000

    while True:
        buf = m.seek(buffer_size, os.SEEK_CUR)
        if not buf:
            break
        


        
if __name__ == "__main__":
        
    if len(sys.argv) > 1:
        outfile = sys.argv[2]
        #CPerf.runAll( outfile )


        # must be overhead in creating file object and then reading from it?
        print( bench_read_file( ))        # 0.003299713134765625

        # # sys.stdin is treated as a file object, but there might be less overhead
        print( bench_read_stdin( ) )      # 0.0073833465576171875

        print( bench_read_bytes( ) )     # 0.0012459754943847656
        
        # # should be covered in a setup method...
        # # takes time to construct memory map
        f = open('samples/large_file.txt', 'r+b')
        m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        print (bench_read_mmap( m ) )      # 4.76837158203125e-06

        
    else:
        print("missing profiler, outfile, and function parameters")
