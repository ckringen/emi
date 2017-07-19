
# general profiling class that CPerf, MPerf and LPerf should inherit from
# should provide basic macro functionality, like running a function on increasingly larger data

class Perf( ):

    def __init__( self ):
        pass

    def swellString( func, rng=1 ):
        ''' wrap a profiled function --which takes a string-- so that we call it on increasingly larger inputs '''
        
        alpha = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,q,x,y,z'.split(',')
        t = ""
        for i in range(rng):
            t += random.choice(alpha)
            func( t )

    def setUp(self):
        pass

    
    def tearDown(self):
        pass

