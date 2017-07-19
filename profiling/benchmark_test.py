

# still need benchmark function-specific imports in here though... possibly a reason to separate
# benchmark functions and benchmark class...
import os
import mmap

class benchmark( ):
    
    def __init__( self, funcs):
        self.setUp( )
        self.global_funcs = funcs

    def runAll( self ):
        print("we're getting called!")
        for item in dir(self):
            if item in self.global_funcs:
                func = getattr(self,item)
                print(func)
                print(func( self, "myoutfile" ))

    def setUp( self ):
        f = open('SampleData/large_file.txt', 'r+b')
        self.mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    def tearDown( self ):
        pass

    
    def bench_read_mmap( self, outfile ):
        ''' read from memory-mapped file by bytes, assuming islice-size and buffer-size are the same '''

        buffer_size = 100000
        
        while True:
            buf = self.mmap_file.seek(buffer_size, os.SEEK_CUR)
            if not buf:
                break
