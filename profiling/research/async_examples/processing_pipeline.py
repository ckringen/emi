
import multiprocessing
import collections
import mmap
import time
# sentinel = None

# # so we can kill the workflow by passing a sentinel through the pipe and
# # catching it down in the main loop.  But I still don't understand when to join
# def readPipe( f, tokeProc ):
#     buffer_size = 10
#     while True:
#         buf = f.read(buffer_size)
#         #print("getting called: ", buf)
#         if not buf:
#             print("breaking")
#             tokeProc.send(sentinel)
#             break
#         tokeProc.send(buf)

        
# if __name__ == '__main__':

#     f = open("../../SampleData/bigram_count.txt", "r")

#     readProc, tokenizeProc = multiprocessing.Pipe(duplex=False)
#     proc = multiprocessing.Process(target=readPipe, args=(f, tokenizeProc) )
#     proc.start()

#     while True:
#         info = readProc.recv( )
#         if info is sentinel:
#             print("we poisoned the pipe!")
#             break
#         else:
#             print( "receiving: ", readProc.recv( ) )

#     # I don't understand what this does
#     proc.join( )

    
# # -----------------------------------------------------------------------------
sentinel = None


#@profile
def producer(f, queue):
    buffer_size = 10000
    while True:
        buf = f.read(buffer_size)
        if not buf:
            # need to send one per worker
            for _ in range(1):
                queue.put(sentinel)
            break        
        queue.put(buf)

        
#@profile        
def tokenizer(in_queue, out_queue, counter):
    while True:

        buf = in_queue.get( )

        if buf is sentinel:
            break

        buf = buf.split( )

        try:
            while buf:
                skip = [(buf[0],buf[2])]
                counter.update( skip )
                del buf[0]

        except IndexError as e:
            pass
                
            # buf = buf.split( )
            # buf = [(buf[0],buf[2])]
            # counter.update( buf )
            # print(counter)
            # # buf = buf.split( )
            
            
def skipgrammer(in_queue, out_queue):
    while True:
        buf = in_queue.get( )
        try:
            while buf:
                if buf is sentinel:
                    out_queue.put(sentinel)
                    break
                else:
                    skip = (buf[0], buf[2])
                    out_queue.put(skip)
                    del buf[0]
        except IndexError as e:
            pass

    
def consumer(queue):
    while True:
        buf = queue.get( )
        if buf is sentinel:
            break
        else:
            c = collections.Counter( buf )
            print(c)
            
    # ans = []
    # for i in iter( queue.get, None):
    #     if i is sentinel:
    #         break
    #     ans.append(i)
    #     #print(i)
    # return ans


# so if we give ourselves 5 processes and read 10000 bytes at a time
# we can process the large file (split the strings) in .17 seconds
#@profile
def main( ):

    #f = open("../../SampleData/large_file.txt","r")
    f = open('../../SampleData/large_file.txt', 'r+b')
    mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    c = collections.Counter( )
    
    in_queue = multiprocessing.Queue()
    out_queue = multiprocessing.Queue()
    #fin_queue = multiprocessing.Queue()

    # producer 
    prod = multiprocessing.Process(target=producer, args=(mmap_file, in_queue))
    tok = multiprocessing.Process(target=tokenizer, args=(in_queue, out_queue, c))

    a = time.time( )
    prod.start()

    # processor
    tok.start( )

    # workers = [ multiprocessing.Process(target=worker, args=(in_queue, out_queue)) for i in range(10) ]
    # for i in workers:
    #     i.start()

    # skip = multiprocessing.Process(target=skipgrammer, args=(out_queue, fin_queue))
    # skip.start( )
    
    # # consumer
    # consum = multiprocessing.Process(target=consumer, args=(fin_queue,))    
    # consum.start( )


    # # endgame play
    # prod.join( )
    # tok.join( )
    b = time.time( )

    print(b-a)

    #skip.join( )
    # consum.join( )
    
    # for w in workers :
    #     print("joining")
    #     w.join( )    
        
    #consum.join( )

    #print(out_queue.get( ) )
    
    #c = collections.Counter( (i for i in out_queue.get( ) ) )
    #print(c)

    
if __name__ == "__main__":
    main( )

# -------------------------------------------------------------------------------
# sentinel=None

# def f2(inq,outq):
#     while True:
#         val=inq.get()
#         if val is sentinel:
#             break
#         outq.put(val*2)

# def f3(outq):
#     while True:
#         val=outq.get()
#         if val is sentinel:
#             break
#         print(val)

# def f1():
#     num_workers=2
#     inq=mp.Queue()
#     outq=mp.Queue()
#     for i in range(5):
#         inq.put(i)
#     for i in range(num_workers):        
#         inq.put(sentinel)
#     workers=[mp.Process(target=f2,args=(inq,outq)) for i in range(2)]
#     printer=mp.Process(target=f3,args=(outq,))
#     for w in workers:
#         w.start()
#     printer.start()
#     for w in workers:
#         w.join()
#     outq.put(sentinel)
#     printer.join()

# if __name__=='__main__':
#     f1()

# # -----------------------------------------------------------------------------
# import multiprocessing
# import hashlib

# class ChecksumPipe(multiprocessing.Process):

#     all_open_parent_conns = []

#     def __init__(self, csname):
#         multiprocessing.Process.__init__(self, name = csname)
#         self.summer = eval("hashlib.%s()" % csname)
#         self.child_conn, self.parent_conn = multiprocessing.Pipe(duplex = False)
#         ChecksumPipe.all_open_parent_conns.append(self.parent_conn)
#         self.result_queue = multiprocessing.Queue(1)
#         self.daemon = True
#         self.start()
#         self.child_conn.close() # This is the parent. Close the unused end.

#     def run(self):
#         for conn in ChecksumPipe.all_open_parent_conns:
#             conn.close() # This is the child. Close unused ends.
#         while True:
#             try:
#                 print "Waiting for more data...", self
#                 block = self.child_conn.recv_bytes()
#                 print "Got some data...", self
#             except EOFError:
#                 print "Finished work", self
#                 break
#             self.summer.update(block)
#         self.result_queue.put(self.summer.hexdigest())
#         self.result_queue.close()
#         self.child_conn.close()

#     def update(self, block):
#         self.parent_conn.send_bytes(block)

#     def hexdigest(self):
#         self.parent_conn.close()
#         return self.result_queue.get()

# def main():
#     # Calculating the first checksum works
#     md5 = ChecksumPipe("md5")
#     md5.update("hello")
#     print "md5 is", md5.hexdigest()

#     # Calculating the second checksum works
#     sha1 = ChecksumPipe("sha1")
#     sha1.update("hello")
#     print "sha1 is", sha1.hexdigest()

#     # Calculating both checksums also works fine now
#     md5, sha1 = ChecksumPipe("md5"), ChecksumPipe("sha1")
#     md5.update("hello")
#     sha1.update("hello")
#     print "md5 and sha1 is", md5.hexdigest(), sha1.hexdigest()

# main()


