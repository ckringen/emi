# run a function that loops a given function some number of times
# meant to be invoked as ???
# run

def swell( func, rng=10 ):
    print("inside swell")
    def newf(*args, **kwargs):
        print("inside newf ", *args, **kwargs)
        alpha = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,q,x,y,z'.split(',')
        t = ""
        for i in range(rng):
            t += random.choice(alpha)
            print("t is ", t)
            #print(type(args[0]))
            minif = args[0]
            minif( t )
        return t
    print("returned newf")
    return newf


#@swell
def benchCounter( long_string  ):
    print("inside benchcounter")
    c = Counter( long_string )
    print(c)
 
#benchCounter("an extra arg")


@swell
def runProf( func ):
    func( )

runProf(benchCounter)


