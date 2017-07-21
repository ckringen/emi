
# profile source code functions; each takes a filename where they will write their results
# could also pass to the decorator... which seems to make more sense

# further, if we use the import hook, we can't manually decorate functions, which we might want to do
# so we'll need to think of a way around that...

import os
import fileinput
import mmap
import asyncio

import itertools
import collections 
import src.count_skipgrams as skip

from profilers.TPerf import timer

# --------------------------------------------------- #
#                   data processing                   #
# --------------------------------------------------- #    
async def tokenizeAsync( s ):
    tokens = s.split( )
    await skipgramAsync( tokens )
    
async def bigramAsync( sep ):
    bigs =  [ ]
    for k,v in enumerate(sep):
        if k == len(sep) - 1:
            break
        else:
            bigs.append((v,sep[k+1]))
    await countAsync( bigs )
    
async def skipgramAsync( tokens  ):        
    its = itertools.tee(tokens, 2)   # so xs is an iterable, such that it can return an iterator
    for i, iterator in enumerate(its):
        for _ in range(i):
            next(iterator)

    for block in zip(*its):
        await flatMapAsync( block )

async def flatMapAsync( blocks ):
    grams = flat( blocks )
    await countAsync( blocks )
    
async def countAsync( lst ):
    c = Counter(lst)
    print(c)
    return c

async def readByChunkAsync( fd ):
    f = fileinput.input(files=(fd))
    while True:
        it = list(itertools.islice(f, 100000 ))      # don't really need to tokenize since we're already list-ifying
        if not it:
            print("we'rebreaking")
            break
        await tokenizeAsync( it[ 0 ] )
        
async def mainAsync( ):
    res = await readByChunkAsync("../../SampleData/bigram_count.txt")

@timer
def bench_pipeline_async( ):
    loop = asyncio.get_event_loop( )
    loop.run_until_complete(mainAsync( ))


# --------------------------------------------------- #
#            reading data sources                     #
# --------------------------------------------------- #        
@timer
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

    
@timer
def bench_read_file( outfile ):
    ''' read from file by iter slice object; suffers from same problem as above '''
    f = fileinput.input(files=("samples/large_file.txt"))
    while True:
        it = list(itertools.islice(f, 100000 ))
        if not it:
            break
    
    
@timer
def bench_read_bytes( outfile ):
    ''' read from file by bytes '''
    with open("samples/large_file.txt") as f:
        while True:
            buf = f.read(100000)
            if not buf:
                break

    
@timer
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
