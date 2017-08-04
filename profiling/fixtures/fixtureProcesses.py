
import multiprocessing
import collections
import mmap

import benchmarking.benchmarking

class benchProcesses( benchmarking.BenchFixture ):
    def __init__( self ):
        self.f = ""
        self.window_size = 2
        self.c = None
        self.in_queue = None
        self.out_queue = None
        self.sentinel = None
        self.setUp( )

    
    def setUp( self ):
        f = open("profiling/SampleData/large_file.txt", 'r+b')
        self.f = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)        
        self.c = collections.Counter( )        
        self.in_queue = multiprocessing.Queue()
        self.out_queue = multiprocessing.Queue()
    
    def tearDown( self ):
        pass

    
    def producer(self, f, queue):
        buffer_size = 10000
        while True:
            buf = self.f.read(buffer_size)
            if not buf:
                for _ in range(1):
                    queue.put(self.sentinel)
                    break        
            queue.put(buf)

                
    def tokenizer(self, in_queue, out_queue, counter):
        while True:
            buf = in_queue.get( )
            if buf is self.sentinel:
                break            
            buf = buf.split( )
            try:
                while buf:
                    skip = [(buf[0],buf[2])]
                    self.c.update( skip )
                    del buf[0]                    
            except IndexError as e:
                pass
            
            
    def skipgrammer(self, in_queue, out_queue):
        while True:
            buf = in_queue.get( )
            try:
                while buf:
                    if buf is self.sentinel:
                        out_queue.put(self.sentinel)
                        break
                    else:
                        skip = (buf[0], buf[2])
                        out_queue.put(skip)
                        del buf[0]
            except IndexError as e:
                pass

    
    def consumer(self, queue):
        while True:
            buf = queue.get( )
            if buf is self.sentinel:
                break
            else:
                c = collections.Counter( buf )
                

    def runPipe( self, outfile ):
        prod = multiprocessing.Process(target=self.producer, args=(self.f, self.in_queue))
        tok = multiprocessing.Process(target=self.tokenizer, args=(self.in_queue, self.out_queue, self.c))

        prod.start()
        tok.start( )

        # endgame play
        prod.join( )
        tok.join( )

    
if __name__ == "__main__":
    benchmarking.Benchmark( )


