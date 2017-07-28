
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

        
if __name__ == "__main__":
    benchmarking.Benchmark( )
