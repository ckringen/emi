
import line_profiler

def add2(n):
    return n + 2
add2 = line_profiler.LineProfiler(add2)

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next( cr )
        return cr
    return start


def producer( text, target ):
    target.send( text )

    
@coroutine    
def filterer( target ):
    while True:
        res = (yield)
        res = res.split( )
        target.send(res)

        
@coroutine    
def consumer( ):
    while True:
        res = (yield)
        print(res)

        
if __name__ == '__main__':
    
    t = "here is some delicious text."

    lp = line_profiler.LineProfiler( producer, filterer, consumer )
    lp.enable_by_count( )
        
    producer( t,
              filterer( 
                  consumer( ) ) )

    lp.disable_by_count( )

    lp.print_stats( )
    
    #  dump_stats(filename) method will pickle the results out to the given file.
    # print_stats([stream]) prints the formatted results to sys.stdout or whatever stream you specify.
    # get_stats() will return LineStats object, a dictionary containing the results and the timer unit.
