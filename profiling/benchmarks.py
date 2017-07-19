
# profile source code functions; each takes a filename where they will write their results
# could also pass to the decorator... which seems to make more sense

# further, if we use the import hook, we can't manually decorate functions, which we might want to do
# so we'll need to think of a way around that...

import os
import fileinput
import mmap
#import asyncio

import itertools
import collections 
import src.count_skipgrams as skip


# --------------------------------------------------- #
#                   data processing                   #
# --------------------------------------------------- #    
#@CPerf
def bench_ichunks( outfile ):
    s = "dog's running real fast, I tell you hwat"
    count_skipgrams.ichunks( s, 3 )


#@CPerf
def bench_tee( outfile ):
    its = itertools.tee(xs, window_size)
    for i, iterator in enumerate(its):
        for _ in range(i):
            next(iterator)

            
#@CPerf
def bench_tokenizeSmallString( outfile ):
    s = "dog's running real fast, I tell you hwat"
    count_skipgrams.tokenize( s )
    

#@CPerf
def bench_islice( outfile ):
    myiter = itertools.islice(sys.stdin, 100000)

    
#@CPerf
def bench_flat( outfile ):
    lst = [['a','b'],'c',['d'], [['e','f'],['g'],['h']],'i',[[[[[['j']]]]]]]
    itertools.chain.from_iterable( lst )

    
#@CPerf
def bench_from_iterable( outfile ):
    grams = flat(map(get_count_skipgrams, map(tokenize, lines)))

    
#@CPerf
def bench_get_skipgrams( outfile ):
    tokens = ['<s>', 'Here', 'Here', 'is', 'is', 'is', 'a', 'a', 'a', 'a', 'is', 'a', 'is', 'a', 'fairly', 'good', 'good', 'fairly', 'example', 'of', 'example', 'of', 'a', 'piece', 'of', 'text', 'of', 'text.', '</s>']
    gen = map(count_skipgrams.get_skipgrams, tokens)



# --------------------------------------------------- #
#            reading data sources                     #
# --------------------------------------------------- #        
#@timer
def bench_read_stdin( outfile ):
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

    
#@timer
def bench_read_file( outfile ):
    ''' read from file by iter slice object; suffers from same problem as above '''
    f = fileinput.input(files=("samples/large_file.txt"))
    while True:
        it = list(itertools.islice(f, 100000 ))
        if not it:
            break
    
    
#@timer
def bench_read_bytes( outfile ):
    ''' read from file by bytes '''
    with open("samples/large_file.txt") as f:
        while True:
            buf = f.read(100000)
            if not buf:
                break

    
#@timer
def bench_read_mmap( mmap_file, outfile ):
    ''' read from memory-mapped file by bytes, assuming islice-size and buffer-size are the same '''

    buffer_size = 100000

    while True:
        buf = mmap_file.seek(buffer_size, os.SEEK_CUR)
        if not buf:
            break
        


# --------------------------------------------------- #
#                 whole pipeline                      #
# --------------------------------------------------- #        
