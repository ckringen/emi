
import multiprocessing
import collections
import mmap

import benchmarking

class benchProcesses( benchmarking.BenchFixture ):
    def __init__( self ):
        pass
    
    def setUp( self ):
        f = open('../../SampleData/large_file.txt', 'r+b')
        mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)        
        c = collections.Counter( )        
        in_queue = multiprocessing.Queue()
        out_queue = multiprocessing.Queue()

        sentinel = None

    
    def tearDown( self ):
        pass

    
    def producer(self, f, queue):
        buffer_size = 10000
        while True:
            buf = f.read(buffer_size)
            if not buf:
                # need to send one per worker
                for _ in range(1):
                    queue.put(sentinel)
                    break        
                queue.put(buf)

                
    def tokenizer(self, in_queue, out_queue, counter):
        while True:
            buf = in_queue.get( )
            if buf is sentinel:
                break            
            buf = buf.split( )            
            try:
                while buf:
                    skip = [(buf[0],buf[2])]
                    counter.update( skip )
                    del buf[0]                    
            except IndexError as e:
                pass
            
            
    def skipgrammer(self, in_queue, out_queue):
        while True:
            buf = in_queue.get( )
            try:
                while buf:
                    if buf is sentinel:
                    out_queue.put(sentinel)
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
            if buf is sentinel:
                break
            else:
                c = collections.Counter( buf )
                

    def runPipe( self ):
        prod = multiprocessing.Process(target=producer, args=(mmap_file, in_queue))
        tok = multiprocessing.Process(target=tokenizer, args=(in_queue, out_queue, c))

        prod.start()
        tok.start( )

        # # endgame play
        # prod.join( )
        # tok.join( )

    
if __name__ == "__main__":
    benchmark.Benchmark( )


