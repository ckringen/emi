
# chain data processing steps together via asynchronous coroutines instead of generators on the stack
# kind of works!

import time
import asyncio

import fileinput
import itertools

from collections import Counter
from src import count_skipgrams as skip


# --------------------------------------------------- #
#               asynchronous pipeline                 #
# --------------------------------------------------- #    
async def tokenizeAsync( s ):
    tokens = s.split( )
    await bigramAsync( tokens )


    
async def bigramAsync( sep ):
    bigs =  [ ]
    for k,v in enumerate(sep):
        if k == len(sep) - 1:
            break
        else:
            bigs.append((v,sep[k+1]))
    await countAsync( bigs )



    
async def readByChunkAsync( fd ):
    f = fileinput.input(files=(fd))
    while True:
        it = list(itertools.islice(f, 100000 ))      # don't really need to tokenize since we're already list-ifying
        if not it:
            print("we'rebreaking")
            break
        print("it is ", it[0])
        await tokenizeAsync( it[ 0 ] )
        
async def countAsync( lst ):
    c = Counter(lst)
    print(c)
    return c


async def mainAsync( ):
    res = await readByChunkAsync("../samples/bigram_count.txt")
    


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



