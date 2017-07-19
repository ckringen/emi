
# parse commandline of importhook.py to grab which functions should be decorated with which performance profilers
# need to figure out how to pass back info to import hook; current seems suboptimal...

import argparse

def parseCommandLine( ):

    tperf = []
    cperf = []

    parser = argparse.ArgumentParser( )

    parser.add_argument("-t", "--TPerf", help="use the timer function from the TPerf module" )
    parser.add_argument("-c", "--CPerf", help="use the cProfiler from the CPerf module" )
    
    args = parser.parse_args( )
    
    tperf.append(args.TPerf)
    cperf.append(args.CPerf)

    res = [tperf,cperf]
    
    return res

