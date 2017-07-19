
# wrapper around memory_profiler

from memory_profiler import profile

class CPerf( ):

    def __init__(self, outfile="logging.out", benchmarks=[]):
        self.outfile = outfile
        self.benchmarks = benchmarks

        
    def logAsCSV( self, profiler="c" ):
        fd = open(self.outfile,"w")
        return fd

            
    def getFunctions( self ):
        for i in self.benchmarks:
            if i in perf.__dict__:
                <do something>

    def runBenchmarks( self ):

        fd = logAsCSV( )
        
        b = getFunctions( )

        a = prrofile(getattr(p,i)), stream=fd)
        a( ) 


        
    def setUp(self):
        pass

    
    def tearDown(self):
        pass

