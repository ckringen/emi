
# chain data processing steps together via asynchronous coroutines instead of generators on the stack

#from memory_profiler import profile
import os
import time
import asyncio

import mmap
import fileinput
import itertools

import collections
from src import count_skipgrams as skip


# --------------------------------------------------- #
#               synchronous pipeline                 #
# --------------------------------------------------- #    
def tokenize( s ):
    tokens = s.split( )
    return tokens


def readByChunk( fd ):
    f = fileinput.input(files=(fd))
    words = []
    while True:
        it = list(itertools.islice(f, 100000 ))      # don't really need to tokenize since we're already list-ifying
        if not it:
            break
        word = tokenize( it[0] )
        print("word is ", word)
        words.append(word)

    ans = count( words )
    return ans
        
def count( lst ):
    lst = lst[0]
    c = collections.Counter(lst)
    print(c)
    return c


def main( ):
    res = readByChunk("../samples/large_file.txt")

    
# --------------------------------------------------- #
#               asynchronous pipeline                 #
# --------------------------------------------------- #    
# need to read up to a space: read buf size, check if space, if not, read from there until space, concatenate strings;
# a tad unwieldy
async def mmapAsync( mmap_file ): #, q, overall ):
    buffer_size = 100000
    while True:
        buf = mmap_file.read(buffer_size)                     
        if not buf:
            break

        # if you read part way into a word, read some more until you hit a space
        if buf[-1] != 32:
            extra = b""
            while True:
                extra_byte = mmap_file.read(1)
                if extra_byte:
                    if extra_byte[0] != 32:
                        extra = extra + extra_byte
                    else:
                        buf = buf + extra + extra_byte
                        break
                else:
                    break

        await tokenizeAsync( buf ) #, q, overall ) 

        
async def tokenizeAsync( s ): #, q, overall ):
    tokens = s.split( )
    #await pushOnQAsync( tokens ) #, q, overall )

    
async def pushOnQAsync( t ): #, q, overall ):
    for i in t:
        q.append(i)    # pushes onto right side
    #await skipgramAsync( ) #q, overall )


# some async magic going on I don't understand here
# if and else will seemingly get triggered (print stmt) in succession...
async def skipgramAsync( ): #q, overall ):
    while True:
        if len(q) > 2:
            await countAsync( (q[0], q[2]) ) #, q, overall )
        else:
            break
        
async def countAsync( tup ):  #, q, overall ):
    #overall = collections.Counter( tup )
    q.popleft( )
    return overall
        
#@profile
async def mainAsync( mmap_file): #, q, overall ):
    await mmapAsync( mmap_file ) #, q, overall )

overall = collections.Counter( )

if __name__ == "__main__":

    # mmap file, read chunk, stick in queue, do indexing, pass to counter, pop head, GOTO beginning
    # as is, need to pass around queue and counter object, unsure if this is causing extra work to be done

    # setup
    f = open('../../SampleData/large_file.txt', 'r+b')
    mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    q = collections.deque( )
    #overall = collections.Counter( )

    # asyncio needs "gather" or "ensure_futures" to return values from coroutines,
    # haven't figured out how to make it work yet
    beg = time.time( )
    loop = asyncio.get_event_loop( )
    result = loop.run_until_complete(mainAsync( mmap_file ) ) #, q, overall ))
    end = time.time( )
    print("elapsed: ", end - beg )









    
    # # async     # 0.0074920654296875
    # begin = time.time( )    
    # loop = asyncio.get_event_loop( )
    # loop.run_until_complete(mainAsync( ))
    # end = time.time( )
    
    # print( "elapsed: ", end - begin )


    # # needs bigramming
    # # serial    # 0.010806798934936523
    # begin = time.time( )
    # main( )
    # end = time.time( )
    # print( "elapsed: ", end - begin )

    # begin = time.time( )    
    # f = open("../samples/large_file.txt")
    # skip.main2( f, 0, 100000 ) 
    # end = time.time( )
    
    # print( "elapsed: ", end - begin )



