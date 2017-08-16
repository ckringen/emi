
# general base class for logging benchmarking fixtures

# TODO:
# 1. need different way to call benchmarking functions; register them directly as opposed to by name?
# 2. clean up decorating and registering functions: former is getting called twice
# 3. relative imports??

from inspect import getmembers, ismethod, isclass
import argparse
import datetime
dt = datetime.datetime.now().strftime("%Y%m%d")

from .benchmarkFixture import BenchFixture
from ..profilers.CPerf import CPerf
from ..profilers.TPerf import TPerf
from ..profilers.LPerf import LPerf
from ..profilers.MPerf import MPerf
from ..profilers.DPerf import DPerf


class Benchmark( ):
    def __init__( self, module="__main__" ):
        self.fixture = None
        self.global_funcs = { }
        self.module = module
        self.args = self.parse_commandline( )
        self.runAll = False
        self.loader()
        self.main( )
        
    def parse_commandline( self ):
        parser = argparse.ArgumentParser( )        
        parser.add_argument("-t", "--TPerf", help="use the timer function from the TPerf module", nargs="*" )
        parser.add_argument("-c", "--CPerf", help="use the cProfiler from the CPerf module", nargs="+" )
        parser.add_argument("-l", "--LPerf", help="use the line_profiler function from the LPerf module", nargs="*" )
        parser.add_argument("-m", "--MPerf", help="use the memor_profiler function from the MPerf module", nargs="*" )
        parser.add_argument("-d", "--DPerf", help="use the disassembler function from the dis module", nargs="*" )
        parser.add_argument("-i", "--identifier", help="string to identify runs of a bench fixture, used to construct the outfile names" )
        args = parser.parse_args( )
        return args

    
    def construct_outfilename( self, name, profiler=None, iden="default" ):
        if self.args.identifier:
            iden = self.args.identifier
        if profiler == None:
            ofn = "{}_{}_{}.Perf".format( dt, name, iden)
        else:
            ofn = "{}_{}_{}.{}".format( dt, name, iden, profiler.__name__ )
        return ofn

    
    def add_profiler(self, func_list, profiler ):
        # if you just write a flag with no args, we see "[]" instead of "None",
        # so we assume you want to decorate every function
        if func_list == [ ]:
            func_list = [i for i,k in getmembers(self.fixture) if ismethod(k) and "__" not in i]
            if profiler == LPerf or profiler == MPerf or profiler == CPerf:
                self.runAll = True
                
        for name, val in getmembers(self.fixture):
            if name in func_list:
                setattr( self.fixture, name, profiler(val))
                ofn = self.construct_outfilename( name, profiler)
                self.global_funcs[name] = ofn
            else:
                pass

                
    def decorate_functions( self ):        
        if self.args.CPerf is not None:
            self.add_profiler( self.args.CPerf, CPerf  )
        if self.args.TPerf is not None:
            self.add_profiler( self.args.TPerf, TPerf  )
        if self.args.LPerf is not None:
            self.add_profiler( self.args.LPerf, LPerf  )
        if self.args.MPerf is not None:
            self.add_profiler( self.args.MPerf, MPerf  )
        if self.args.DPerf is not None:
            self.add_profiler( self.args.DPerf, DPerf  )

        
    def loader( self ):
        # import the fixture (as opposed to subclassing it) so we can access functions to decorate
        if isinstance(self.module, str):
            self.mod = __import__(self.module)

        # create fixture instance so we can run its setup method
        for name, val in getmembers(self.mod):
            if isclass(val) and issubclass(val, BenchFixture):
                self.fixture = val( )

        #self.register_functions( )
        self.decorate_functions( )

        
    # need to run functions from the fixture instance
    def runner( self ):
        if self.runAll:
            self.fixture.runPipe( )
        else:
            for name, val in getmembers(self.fixture):
                if name in self.global_funcs:
                    func = getattr(self.fixture,name)
                    outname = self.global_funcs[name]
                    func( outname )

                
    def main( self ):
        self.runner( )

