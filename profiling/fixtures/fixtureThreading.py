
# whole pipeling (reading, tokenizing, skipping, counting) but with threads

import threading
import queue

import collections
import mmap

import benchmarking.benchmarking
import profiling.research.async_examples.threading_pipeline as thread_pipe

class benchThreading( benchmarking.BenchFixture ):
    def __init__( self ):
        self.f = ""
        self.window_size = 2
        self.c = None
        self.setUp( )
    
    def setUp( self ):
        f = open("/home/aik/PersonalProjects/Building46/emi/profiling/SampleData/large_file.txt", 'r+b')
        self.f = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)        
        self.c = collections.Counter( )        
        
    def tearDown( self ):
        pass

    def read_mmap( self ):
        buffer_size = 100000
        while True:
            buf = self.f.read(5)
            if not buf:
                break
            yield buf
            
    def tokenize( self ):
        while True:
            text = (yield)
            text = text.split( )
            try:
                yield [(text[0], text[self.window_size])]
                del text[0]               
            except IndexError as e:
                pass
            
    def count( self ):
        while True:
            sg = (yield)
            self.c.update(sg)
            
    def runPipe( self, outfilename ):
        thread_pipe.Pipeline([self.read_mmap( ), self.tokenize(), self.count()]).run_parallel()

        
if __name__ == "__main__":
    benchmarking.Benchmark( )


