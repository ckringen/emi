
# general base class for logging benchmarking fixtures

import argparse
from inspect import getmembers, ismethod, isclass

from .benchmarkFixture import BenchFixture
from .CPerf import CPerf
from .TPerf import TPerf

import datetime
dt = datetime.datetime.now().strftime("%Y%m%d")


class Benchmark( ):
    def __init__( self, module="__main__" ):
        print("bench init")
        self.fixture = None
        self.global_funcs = { }
        self.module = module
        self.args = self.parse_commandline( )
        self.loader()
        self.main( )
        
    def parse_commandline( self ):
        parser = argparse.ArgumentParser( )        
        parser.add_argument("-t", "--TPerf", help="use the timer function from the TPerf module", nargs="+" )
        parser.add_argument("-c", "--CPerf", help="use the cProfiler from the CPerf module", nargs="+" )
        parser.add_argument("-i", "--identifier", help="string to identify runs of a bench fixture, used to construct the outfile names", nargs="+" )
        args = parser.parse_args( )
        
        if args.CPerf is None and args.TPerf is None:
            return None
        else:
            return args
    
        # decorate functions
        self.register_functions( )

    def construct_outfilename( self, name, profiler=None, iden="default" ):
        if self.args.identifier:
            iden = self.args.identifier[0]
        if profiler == None:
            ofn = "{}_{}_{}.Perf".format( dt, name, iden)
        else:
            ofn = "{}_{}_{}.{}".format( dt, name, iden, profiler.__name__ )
        return ofn

    def add_profiler(self, func_list, profiler ):
        for name, val in getmembers(self.fixture):
            if name in func_list:
                setattr( self.fixture, name, profiler(val))
                ofn = self.construct_outfilename( name, profiler)
                self.global_funcs[name] = ofn
            else:
                pass
                #print( "func not in benchmarks" )

    def decorate_functions( self ):        
        if self.args.CPerf:
            self.add_profiler( self.args.CPerf, CPerf  )
        if self.args.TPerf:
            self.add_profiler( self.args.TPerf, TPerf  )

    # either you provided an explicit list for each profiler, or you provided nothing, which
    # defaults to running all functions (assumption: you decorated the functions in the fixture)
    def register_functions( self ):
        if self.args is None:
            for name, val in getmembers(self.fixture):
                ofn = self.construct_outfilename( name )
                self.global_funcs[name] = ofn
        else:
            self.decorate_functions( )

    def loader( self ):
        # import the fixture (as opposed to subclassing it) so we can access functions to decorate
        if isinstance(self.module, str):
            print( "importing fixture " )
            self.mod = __import__(self.module)

        # create fixture instance so we can run the setup method
        for name, val in getmembers(self.mod):
            if isclass(val) and issubclass(val, BenchFixture):
                self.fixture = val( )

        self.register_functions( )
            
    # need to run functions from the fixture instance
    def runner( self ):
        for name, val in getmembers(self.fixture):
            if name in self.global_funcs:
                func = getattr(self.fixture,name)
                outname = self.global_funcs[name]
                print("outname is: ", outname)
                func( outname )
                
    def main( self ):
        self.runner( )

