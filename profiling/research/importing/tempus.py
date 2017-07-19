
import time

def timer( func ):

    def doTime( *args, **kwargs ):

        begin = time.time( )
        func( *args )
        end = time.time( )
        return end - begin

    return doTime
