
# general base class for logging benchmarking fixtures

import argparse
from inspect import getmembers, ismethod, isclass

from .benchmarkFixture import BenchFixture
from .CPerf import CPerf

import datetime
dt = datetime.datetime.now().strftime("%Y%m%d")


class Benchmark( ):
    def __init__( self, module="__main__" ):
        self.global_funcs = []
        self.module = module
        self.args = self.parse_commandline( )  
        self.loader()
        self.main( )

        
    def parse_commandline( self ):
        parser = argparse.ArgumentParser( )        
        parser.add_argument("-t", "--TPerf", help="use the timer function from the TPerf module", nargs="+" )
        parser.add_argument("-c", "--CPerf", help="use the cProfiler from the CPerf module", nargs="+" )        
        args = parser.parse_args( )
        return args

    
    def loader( self ):
        if isinstance(self.module, str):
            self.mod = __import__(self.module)
        self.register_functions( )

        
    def register_functions( self ):
        if self.args.CPerf:
            for k in self.args.CPerf:
                self.add_profiler( k, CPerf  )

                
    def add_profiler(self, func_list, profiler ):
        for name, val in getmembers(self.mod):
            if isclass(val) and issubclass(val, BenchFixture):
                for n,v in getmembers(val):
                    if n in func_list:
                        setattr( self, n, profiler(v))
                        ofn = "{}_{}.{}".format( dt, name, profiler.__name__ )
                        self.global_funcs.append([n,ofn])
                    else:
                        pass
                    #print( "func not in benchmarks" )


    # somehow need to grab outfile name...
    def runner( self ):
        for item in dir(self):
            if item in self.global_funcs[0]:
                func = getattr(self,item)
                print(func)                
                func( )
                # this is weird, I dunno
                #print(func( self, "myoutfile.cperf" ))

                
    def main( self ):
        print("we made it to main!")        
        self.runner( )

