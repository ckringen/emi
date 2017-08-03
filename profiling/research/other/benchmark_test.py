
# import and modify select benchmark functions with appropriate 
# performance decorators, e.g. "bench_read_mmap = CPerf(bench_read_mmap)"
# still need benchmark function-specific imports in here though...
# possibly a reason to separate benchmark functions and benchmark class...

import os
import datetime
import mmap

from inspect import getmembers

from profilers.CPerf import CPerf
from profilers.TPerf import timer


dt = datetime.datetime.now().strftime("%Y%m%d")


class benchmark( ):    
    def __init__( self, *args):
        self.setUp( )

        # can combine these two, I'd imagine
        self.global_funcs = [ ]
        self.registerFunctions( *args )

    def runAll( self ):
        for item in dir(self):
            if item in self.global_funcs:
                func = getattr(self,item)
                #print(func)
                
                # this is weird, I dunno
                print(func( self, "myoutfile.cperf" ))

                
    # need to fix path specification
    def setUp( self ):
        f = open('./profiling/SampleData/large_file.txt', 'r+b')
        self.mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    def tearDown( self ):
        pass

    def registerFunctions( self, args ):

        outfile_names = []
        for k, func_list in enumerate(args):
            if func_list:
                if k == 0:
                    n = self.addProfiler(func_list, timer )
                    outfile_names.append(n)
                elif k == 1:
                    n = self.addProfiler(func_list, CPerf )
                    outfile_names.append(n)
                else:
                    del func_list[k]
                    print( "more items than profilers" )
        #both = zip(func_list,outfile_names)
        #self.global_funcs.extend(both)
        self.global_funcs.extend( func_list)

    def addProfiler(self, func_list, profiler ):
        for name, value in getmembers(self):
            if name in func_list:
                setattr( self, name, profiler(value))
                ofn = "{}_{}.{}".format(dt, name, profiler.__name__ )                
            else:
                pass
                #print( "func not in benchmarks" )
        # return list of outfile names
                
    def bench_read_mmap( self ):
        ''' read from memory-mapped file by bytes ''' 
        buffer_size = 100000        
        while True:
            buf = self.mmap_file.seek(buffer_size, os.SEEK_CUR)
            if not buf:
                break
