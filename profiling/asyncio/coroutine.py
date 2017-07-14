
# this kind of works!

import time
import fileinput
import itertools
from collections import Counter
import asyncio

async def tokenizeAsync( s ):
    tokens = s.split( )
    await countAsync( tokens )

async def readByChunkAsync( fd ):
    f = fileinput.input(files=(fd))
    while True:
        it = list(itertools.islice(f, 100000 ))      # don't really need to tokenize since we're already list-ifying
        if not it:
            break
        await tokenizeAsync( it[ 0 ] )
        
async def countAsync( lst ):
    c = Counter(lst)
    print(c)
    return c


async def mainAsync( ):
    res = await readByChunkAsync("../samples/large_file.txt")
    


# ------- serial ----- #
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
        words.append(word)

    ans = count( words )
    return ans
        
def count( lst ):
    lst = lst[0]
    c = Counter(lst)
    print(c)
    return c


def main( ):
    res = readByChunk("../samples/large_file.txt")

if __name__ == "__main__":

    # async     # 0.0074920654296875
    begin = time.time( )    
    loop = asyncio.get_event_loop( )
    loop.run_until_complete(mainAsync( ))
    end = time.time( )
    
    print( "elapsed: ", end - begin )

    
    # serial    # 0.010806798934936523
    begin = time.time( )
    main( )
    end = time.time( )

    print( "elapsed: ", end - begin )




