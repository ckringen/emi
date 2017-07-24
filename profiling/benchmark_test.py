
# import and modify select benchmark functions with appropriate 
# performance decorators, e.g. "bench_read_mmap = CPerf(bench_read_mmap)"
# still need benchmark function-specific imports in here though...
# possibly a reason to separate benchmark functions and benchmark class...

import os
import datetime
import mmap

from inspect import getmembers, isclass, ismethod

from profilers.CPerf import CPerf
from profilers.TPerf import timer


class benchmark( ):    
    def __init__( self, *args):
        self.setUp( )
        self.global_funcs = [ ]
        self.registerFunctions( *args )

    def runAll( self ):
        print("we're getting called! ", self.global_funcs)
        for item in dir(self):
            if item in self.global_funcs:
                func = getattr(self,item)
                print(func)

                # this is weird, I dunno
                print(func( self, "myoutfile.cperf" ))

    # need to fix path specification
    def setUp( self ):
        f = open('./profiling/SampleData/large_file.txt', 'r+b')
        self.mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    def tearDown( self ):
        pass

    def registerFunctions( self, args ):
        for k, func_list in enumerate(args):
            if func_list:
                if k == 0:
                    self.addProfiler(func_list, timer )
                elif k == 1:
                    self.addProfiler(func_list, CPerf )
                else:
                    print( "more items than profilers" )
        self.global_funcs.extend( func_list)

    def addProfiler(self, func_list, profiler ):
        for name, value in getmembers(self):
            if name in func_list:
                setattr( self, name, profiler(value))
            else:
                pass
                #print( "func not in benchmarks" )
                
    def bench_read_mmap( self, outfile ):
        ''' read from memory-mapped file by bytes ''' 
        buffer_size = 100000        
        while True:
            buf = self.mmap_file.seek(buffer_size, os.SEEK_CUR)
            if not buf:
                break
