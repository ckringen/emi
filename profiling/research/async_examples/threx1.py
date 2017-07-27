
import threading
import queue
import time

def tokenize( ):
    while True:
        yield (a[0],a[2])
        del a[0]


def producer( condition, value ):
    with condition:
        items.append( value )
        condition.notify( )

def consumer( condition ):
    with condition:
        while not items:
            condition.wait( )
        x = items.pop(0)
        print( "consumed: ", x )
    
def threader( ):
    while True:
        worker = q.get( )
        tokenize(worker)
        q.task_done( )

def decrease( n ):
    while n > 0:
        yield n
        n -= 1
        
if __name__ == "__main__":

    # items = [ ]
    # items_cv = threading.Condition( )
        
    # x = threading.Thread(target=consumer, args=(items_cv,))
    # y = threading.Thread(target=consumer, args=(items_cv,))
    # z = threading.Thread(target=producer, args=(items_cv, 5))

    # x.daemon = True
    # y.daemon = True
    # z.daemon = True
    
    # z.start()
    # x.start()
    # y.start()

    a = '''this is a this is bytes bytes file file file to test bigram bigram counting.
    for what it's worth worth here is some more tasty data.'''.split( )
    
    for i in tokenize( ):
        print( i )
