
import itertools
import collections
import asyncio

import benchmarking

class benchAsync( benchmarking.BenchFixture ):
    def __init__( self ):
        pass
    
    def setUp( ):
        pass
    
    def tearDown( ):
        pass
    
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
        c = collections.Counter(lst)
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

    #@timer
    def bench_pipeline_async( ):
        loop = asyncio.get_event_loop( )
        loop.run_until_complete(mainAsync( ))





async def mmapAsync( mmap_file ): #, q, overall ):
    buffer_size = 100000
    while True:
        buf = mmap_file.read(buffer_size)                     
        if not buf:
            break

        # # if you read part way into a word, read some more until you hit a space
        # if buf[-1] != 32:
        #     extra = b""
        #     while True:
        #         extra_byte = mmap_file.read(1)
        #         if extra_byte:
        #             if extra_byte[0] != 32:
        #                 extra = extra + extra_byte
        #             else:
        #                 buf = buf + extra + extra_byte
        #                 break
        #         else:
        #             break

        async def tokenizeAsync( s ): #, q, overall ):
    tokens = s.split( )
    await pushOnQAsync( tokens ) #, q, overall )

    
async def pushOnQAsync( t ): #, q, overall ):
    for i in t:
        q.append(i)    # pushes onto right side
    await skipgramAsync( ) #q, overall )


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

        
        
if __name__ == "__main__":
    benchmarking.Benchmark( )
