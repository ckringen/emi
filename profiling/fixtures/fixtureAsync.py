
import itertools
import collections
import asyncio

import benchmarking

class benchAsync( benchmarking.BenchFixture ):
    def __init__( self ):
        self.f = ""
        self.deq = None
        self.window_size = 2
        self.setUp( )
            
    def setUp( self ):
        f = open('profiling/SampleData/large_file.txt', 'r+b')
        self.f = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        self.deq = collections.deque( )
    
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
    
    async def countAsync1( lst ):
        c = collections.Counter(lst)
        print(c)
        return c
        
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

    async def tokenizeAsync2( s ): 
        tokens = s.split( )
        await pushOnQAsync( tokens ) 

    
    async def pushOnQAsync( t ): 
        for i in t:
            q.append(i) 
            await skipgramAsync( )


    async def skipgramAsync2( ):
        while True:
            if len(q) > 2:
                await countAsync( (q[0], q[2]) )
            else:
                break
        
    async def countAsync2( tup ):
        q.popleft( )
        return overall
        
    async def mainAsync( mmap_file): 
        await mmapAsync( mmap_file ) 


    def runPipe( self ):
        loop = asyncio.get_event_loop( )
        result = loop.run_until_complete(mainAsync( self.f ) )
            

if __name__ == "__main__":
    benchmarking.Benchmark( )
