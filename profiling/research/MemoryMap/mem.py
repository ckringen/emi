
# memory map a large file

import os
import time
import mmap

def exampleRead( ):
    with open('NUT_DATA.txt', 'r') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ ) as m:
            print( 'First 10 bytes via read :', m.read(10) )
            print( 'First 10 bytes via slice:', m[:10] )
            print( '2nd   10 bytes via read :', m.read(10) )

            
def binaryRead( ):
    f = open('NUT_DATA.txt', 'r+b')
    buffer_size = 64
    retract_size = -32
    start_time = time.time()
    while True:
        f.seek(buffer_size, os.SEEK_CUR)
        # Process some data starting at the current position
        pass
        f.seek(retract_size, os.SEEK_CUR)
        # Process some data starting at the current position
        pass
        if f.tell() > 1024 * 1024 * 10:
            break

    end_time = time.time()
    f.close()
    print('Normal time elapsed: {0}'.format(end_time - start_time))

def mmapRead( ):
 
    f = open('NUT_DATA.txt', 'r+b')
    m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    buffer_size = 64
    retract_size = -32
    start_time = time.time()
    while True:
        m.seek(buffer_size, os.SEEK_CUR)
        # process some data starting at the current position
        pass
        m.seek(retract_size, os.SEEK_CUR)
        # process some data starting at the current position
        pass
        if m.tell() > 1024 * 1024 * 10:
            break

    end_time = time.time()
    m.close()
    f.close()
    print('mmap time elapsed: {0}'.format(end_time - start_time))


if __name__ == "__main__":

    binaryRead( )

    mmapRead( )





    
