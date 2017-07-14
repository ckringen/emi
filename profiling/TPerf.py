
import time

def timer( func ):
    def newf( *args, **kwargs ):
        a = time.time( )
        func( *args )
        b = time.time ( )
        return( b - a )
    return newf
