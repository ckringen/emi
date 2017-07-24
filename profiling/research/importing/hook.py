
# this fails on importing "asyncio" in the benchmarks_test.py (or whatever it's called
# now)
# this was useful in demonstrating how we can modify a class dynamically by introspection
# though

# take in a list of pairs of function names with profiler names
# decorate each function with its profiler
# usage is: python main.py --CPerf add2
# which should decorate add2 with the CPerf class

import builtins
import sys
from inspect import getmembers, isclass, ismethod

from profilers.TPerf import timer
from profilers.CPerf import CPerf


old_imp = builtins.__import__


# as usual, possibly a better way to do this
def add_attr(mod, *args):
    for name, val in getmembers(mod):

        if isclass(val) and name == "benchmark":

            meths = [i for i in getmembers(val)]

            for n, v in getmembers(val):
                if n in args[1]:
                    setattr( val, n, CPerf(v)) # in val (benchmark_test), change function name (n) to CPerf of function object (v)
                    #setattr( mod, name, timer(val))     # for bare functions

# this will get called on the regular imports inside benchmark, so hack: 
# test if we're looking at benchmarks.py, if so use custom_importer, else use classic
def custom_import(*args, **kwargs):
    
    mod = args[0]
    if not mod:
        return
    else:
        if mod == "benchmark_test":
            #print("custom importing: ", mod)
            tperf = args[1][0]
            cperf = args[1][1]
    
            m = old_imp( mod )
            add_attr( m, tperf, cperf )
            return m
        else:
            #print("we're trying to old-style import: ", mod)
            m = old_imp( mod )
            return m


builtins.__import__ = custom_import


