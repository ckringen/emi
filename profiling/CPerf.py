
# wrapper around cProfile
# needs to be redesigned

import cProfile
import pstats

class CPerf( ):
    ''' global state object to hold all benchmark functions, plus some utility
        methods for running and formatting according to the cProfiler 
    '''    

    benches = []    # list of all functions to be profiled, decorators stick them here
    outfile = []    # can't be a string, since immutable
    
    def __init__(self, function, out="logging.out"):
        ''' registers a function in the overall state object '''
        self.outfile.append(out)
        self.benches.append(function)
        self.func = function


    def __call__( self, *args ):
        ''' instance of class getting called triggers this, i.e. a decorated function '''
        s = cProfile.Profile()
        s.enable( )
        self.func( )
        s.disable( )

        logAsCSV( s )

        
    @classmethod
    def runAll( cls, *args, **kwargs ):
        ''' run the "benchmark suite" '''
        for benchmark in cls.benches:
            stats = cProfile.Profile()
            stats.enable( )
            benchmark( )
            stats.disable( )

            cls.printCSV( stats, *args )
            # print( )
            # cls.printPstats( stats, *args )
            

    # # --- printing methods --- # # 
    @classmethod
    def printPstats( cls, stats, fname ):
        ''' the output you get from pstats, left in because I'm positive the csv option is innacurate ''' 
        p = pstats.Stats(stats)
        p.print_stats()

        
    @classmethod
    def label(cls, code):
        ''' holdover from the inner workings of cProfile.py '''
        if isinstance(code, str):
            return ('~', 0, code)    # built-in functions ('~' sorts at the end)
        else:
            return (code.co_filename, code.co_firstlineno, code.co_name)
        
    @classmethod
    def printCSV( cls, stats, fname ):

        fd = open(fname,"w")        
        header = '\t'.join('ncalls,tottime,percall,cumtime,percall\tfilename:lineno(function)\n'.split(','))
        
        flist = stats.getstats( )
        if flist:
            fd.write(header)
            for func in flist:
                l = cls.getLine(func, flist)
                fd.write( l )
    
    @classmethod
    def getLine(cls, func, stats): 
        func_name = cls.label(func.code)
        nc = func.callcount         # ncalls column of pstats (before '/')
        cc = nc - func.reccallcount # ncalls column of pstats (after '/')
        tt = func.inlinetime        # tottime column of pstats
        ct = func.totaltime         # cumtime column of pstats
        
        c = str(nc)

        if nc != cc:
            c = c + '/' + str(cc)
        if nc == 0:
            frac1 = 0
        else:
            frac1 = tt/nc
        if cc == 0:
            frac2 = 0
        else:
            frac2 = ct/cc

        numeric = '\t'.join(map(str, [c,tt,frac1,ct,frac2] ))
        numeric += '\t' + func_name[2] + '\n'
        return numeric
        

