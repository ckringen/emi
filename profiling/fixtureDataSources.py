
import os
import fileinput
import mmap

import benchmarking


class benchDataSources( benchmark.BenchFixture ):
    def __init__( self ):
        pass

    def tearDown( ):
        pass
    
    # need to fix path specification
    def setUp( self ):
        f = open('./profiling/SampleData/large_file.txt', 'r+b')
        self.mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        
    def bench_read_stdin( outfile ):
        ''' read from sys.stdin by iter slice object, possible overhead in converting islice to list; this is done
        because to avoid an infinite loop wherein islice returns an iterator on an empty iterator the same it would on
        a nonempty iterator; https://stackoverflow.com/questions/44986908/yielding-islice-from-reading-file'''
        f = sys.stdin
        sentinel = object( )

        # choose whichever has less overhead
        # a.
        while True:
            it = list(itertools.islice(f, 1, 200 ))
            if not it:
                break
        # b.
        # while True:
        #     it = itertools.islice(f, 1, 200 )
        #     print([i for i in it])
        #     if next(it,sentinel) is sentinel:
        #         break

    
    def bench_read_file( outfile ):
        ''' read from file by iter slice object; suffers from same problem as above '''
        f = fileinput.input(files=("samples/large_file.txt"))
        while True:
            it = list(itertools.islice(f, 100000 ))
            if not it:
                break
    
    
    def bench_read_bytes( outfile ):
        ''' read from file by bytes '''
        with open("samples/large_file.txt") as f:
            while True:
                buf = f.read(100000)
                if not buf:
                    break

    
    def bench_read_mmap( mmap_file, outfile ):
        ''' read from memory-mapped file by bytes, assuming islice-size and buffer-size are the same '''
        
        buffer_size = 100000
        
        while True:
            buf = mmap_file.seek(buffer_size, os.SEEK_CUR)
            if not buf:
                break
        

if __name__ == "__main__":
    benchmarking.Benchmark( )
