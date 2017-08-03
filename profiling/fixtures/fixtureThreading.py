
import threading
import queue
import collections
import mmap

import benchmarking

class benchThreading( benchmarking.BenchFixture ):
    def __init__( self ):
        pass
    
    def setUp( self ):
        f = open('../../SampleData/large_file.txt', 'r+b')
        mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)        
        c = collections.Counter( )        
        window_size = 2

        
    def tearDown( self ):
        pass


    def read_mmap( self ):
        buffer_size = 100000
        while True:
            buf = f.read(5)
            if not buf:
                break
            yield buf

            
    def tokenize( self ):
        while True:
            text = (yield)
            text = text.split( )
            try:
                yield [(text[0], text[window_size])]
                del text[0]               
            except IndexError as e:
                pass

            
    def count( self ):
        while True:
            sg = (yield)
            c.update(sg)

            
    def runPipe( self ):
        Pipeline([read_mmap( ), tokenize(), count()]).run_parallel()

        
if __name__ == "__main__":
    benchmark.Benchmark( )


