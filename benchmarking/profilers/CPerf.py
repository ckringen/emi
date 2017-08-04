
# decorator class, thin wrapper around cProfile

# TODO:
# clean up printing machinery

import cProfile
import pstats

class CPerf( ):
    ''' global state object to hold all benchmark functions, plus some utility
        methods for running and formatting according to the cProfiler 
    '''    
    
    def __init__(self, function, out="logging.out"):
        ''' registers a function in the overall state object '''
        self.func = function


    def __call__( self, *args ):
        ''' triggered by instance of class getting called, i.e. a decorated function '''
        s = cProfile.Profile()
        s.enable( )

        print("running self.func ", self.func)
        self.func( self )

        s.disable( )
        self.printCSVInstance(s,args[0])

        # p = pstats.Stats(s)
        # p.print_stats()

        
    def labelInstance(self, code):
        ''' holdover from the inner workings of cProfile.py '''
        if isinstance(code, str):
            return ('~', 0, code)    # built-in functions ('~' sorts at the end)
        else:
            return (code.co_filename, code.co_firstlineno, code.co_name)

        
    def getLineInstance(self, func, stats): 
        func_name = self.labelInstance(func.code)
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

    
    def printCSVInstance( self, stats, fname ):
        fd = open(fname,"w")
        header = 'ncalls,tottime,percall,cumtime,percall\tfilename:lineno(function)\n'.split(',')
        header = '\t'.join( header )        
        flist = stats.getstats( )
        if flist:
            fd.write(header)
            for func in flist:
                l = self.getLineInstance(func, flist)
                fd.write( l )
