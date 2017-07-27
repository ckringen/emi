from  itertools import islice
import collections

def first_send( ):
    #z = [islice(["here","is","some","text"],i,None) for i in range(2)]
    objs = [ ('here', 'is') ] #, ('is', 'some'), ('some', 'text') ]
    c.update(objs)

        
def second_send( ):
    p = zip(["more","text"])
    c.update(p)
    
if __name__ == "__main__":

    c = collections.Counter( )
    first_send( )
    second_send( )

    print( c )
