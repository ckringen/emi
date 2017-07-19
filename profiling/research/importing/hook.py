
# take in a list of pairs of function names with profiler names
# decorate each function with its profiler
# usage is: python main.py --CPerf add2
# which should decorate add2 with the CPerf class

import builtins
from inspect import getmembers, isclass, ismethod

from profilers.TPerf import timer
from profilers.CPerf import CPerf


old_imp = builtins.__import__


def add_attr(mod, *args):
    for name, val in getmembers(mod):
        if name in args[0]:
            print(val, name, timer(val))
            setattr( mod, name, timer(val))    


# this will get called on the regular imports inside benchmark, so hack: 
# test if we're looking at benchmarks.py, if so use custom_importer, else use classic
def custom_import(*args, **kwargs):

    mod = args[0]
    if not mod:
        return
    else:
        if mod == "benchmarks":
            tperf = args[1][0]
            cperf = args[1][1]
    
            m = old_imp( mod )
            add_attr( m, tperf, cperf )
            return m
        else:
            print("we're trying to old-style import: ", mod)
            m = old_imp( mod )
            return m


builtins.__import__ = custom_import

