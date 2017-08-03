

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next( cr )
        return cr
    return start


def producer( text, target ):
    target.send( text )

    
@coroutine    
def filter( target ):
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
    producer( t,
              filter( 
                  consumer( ) ) )
