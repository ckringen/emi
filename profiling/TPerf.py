
# just wrap benchmark functions for now; could/should be turned into its own class a la CPerf

import time

def timer( func ):
    def newf( *args, **kwargs ):
        a = time.time( )
        func( *args )
        b = time.time ( )
        return( b - a )
    return newf
