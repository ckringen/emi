
import os
import fileinput
import mmap
import collections

import benchmarking
import pipeline

class benchPipe( benchmarking.BenchFixture ):

    def __init__( self ):
        print("pipe init" )
        self.setUp( )
    
    def setUp( self ):

        # memory map the file
        f = open('/home/aik/PersonalProjects/Building46/emi/profiling/SampleData/large_file.txt', 'r+b')
        self.mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        # construct the pipeline object
        self.pipe = pipeline.Pipeline([self.tokenize(), self.count()])

        # count_skipgrams-specific parameters
        self.c = collections.Counter( )
        self.window_size = 2

        
    def tearDown( self ):
        pass

    def tokenize( self ):
        while True:
            print("producing tokens")
            if len(a) == self.window_size:
                break
            else:
                yield [(a[0], a[self.window_size])]
                del a[0]

    def count( self ):
        while True:
            sg = (yield)
            print("counting values", sg)
            self.c.update(sg)

    def bench_read_mmap( mmap_file, outfile ):
        ''' read from memory-mapped file by bytes, assuming islice-size and buffer-size are the same '''
        buffer_size = 100000        
        while True:
            buf = mmap_file.seek(buffer_size, os.SEEK_CUR)
            if not buf:
                break

    # once decorated, "self" refers to the profiler object, not the benchFixture object!
    def count_skipgrams( self ):
        print("fixture Pipelining count skipgrams ", self)
        self.pipe.run_parallel()

        
if __name__ == "__main__":

    print("inside main of fixture pipeline")
    benchmarking.Benchmark( )


        def skipgramProcess( ):   
        while True:
            text = (yield)
            text = text.split( )
            try:
                executor = concurrent.futures.ProcessPoolExecutor(max_workers=10)
                copies = itertools.repeat(text,len(text))
                skips = range(0,len(text),window_size)
                
                for idx, bigram in zip(skips, executor.map(skip, skips, copies)):
                    #print('%d idx has as skips: %s' % (idx, bigram))
                    deq.append( bigram )
                    
            except IndexError as e:
                pass #print(e)


            @coroutine
def skipgramThread( ):   
    while True:
        text = (yield)
        text = text.split( )
        try:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
            copies = itertools.repeat(text,len(text))
            skips = range(0,len(text),window_size)

            for idx, bigram in zip(skips, executor.map(skip, skips, copies)):
                #print('%d idx has as skips: %s' % (idx, bigram))
                deq.append( bigram )
            
        except IndexError as e:
            pass #print(e)
    def skip( idx, text ):
        offset = 2
        bigram = [(text[idx], text[idx+offset])]
        return bigram
