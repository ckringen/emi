
import itertools

words = '''dog cat eats many fish trees vehicles subordinately urban dwellers'''.split( )

explode = itertools.product( words, words )

for k,v in enumerate( explode ):
    
    f = open( "testfile{}.txt".format( k ), "w" )    
    f.write( "{0} {1}\n".format( v[ 0 ], v[ 1 ] ) )
    f.close( ) 



