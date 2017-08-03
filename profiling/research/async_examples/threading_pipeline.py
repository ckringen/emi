>"""Simple but robust implementation of generator/coroutine-based
pipelines in Python. The pipelines may be run either sequentially
(single-threaded) or in parallel (one thread per pipeline stage).

This implementation supports pipeline bubbles (indications that the
processing for a certain item should abort). To use them, yield the
BUBBLE constant from any stage coroutine except the last.

In the parallel case, the implementation transparently handles thread
shutdown when the processing is complete and when a stage raises an
exception.
"""
from __future__ import with_statement # for Python 2.5
from queue import Queue
from threading import Thread, Lock

BUBBLE = '__PIPELINE_BUBBLE__'
POISON = '__PIPELINE_POISON__'

DEFAULT_QUEUE_SIZE = 16

class PipelineError(object):
    """An indication that an exception occurred in the pipeline. The
    object is passed through the pipeline to shut down all threads
    before it is raised again in the main thread.
    """
    def __init__(self, exc):
        self.exc = exc

class FirstPipelineThread(Thread):
    """The thread running the first stage in a parallel pipeline setup.
    The coroutine should just be a generator.
    """
    def __init__(self, coro, out_queue):
        super(FirstPipelineThread, self).__init__()
        self.coro = coro
        self.out_queue = out_queue
        
        self.abort_lock = Lock()
        self.abort_flag = False
    
    def run(self):
        while True:
            # Time to abort?
            with self.abort_lock:
                if self.abort_flag:
                    break
            
            # Get the value from the generator.
            try:
                msg = next(self.coro)
                #print("first pipeline msg: ", msg )
            except StopIteration:
                break
            except Exception as exc:
                #print("exception is: ", exc)
                self.out_queue.put(PipelineError(exc))
                return
            
            # Send it to the next stage.
            self.out_queue.put(msg)
            if msg is BUBBLE:
                continue
        
        # Generator finished; shut down the pipeline.
        self.out_queue.put(POISON)
    
    def abort(self):
        """Shut down the pipeline by canceling this thread and
        poisoning out_channel.
        """
        with self.abort_lock:
            self.abort_flag = True

class MiddlePipelineThread(Thread):
    """A thread running any stage in the pipeline except the first or
    last.
    """
    def __init__(self, coro, in_queue, out_queue):
        super(MiddlePipelineThread, self).__init__()
        self.coro = coro
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        # Prime the coroutine.
        next(self.coro)
        
        while True:
            # Get the message from the previous stage.
            msg = self.in_queue.get()
            #print("middle inq is: ", msg )
            if msg is POISON:
                break
            elif isinstance(msg, PipelineError):
                self.out_queue.put(msg)
                return
            
            # Invoke the current stage.
            try:    
                #print(self.coro.__name__)
                out = self.coro.send(msg)
            except Exception as exc:
                #print(exc.__cause__)
                self.out_queue.put(PipelineError(exc))
                return
            
            # Send message to next stage.
            if out is BUBBLE:
                continue
            self.out_queue.put(out)
        
        # Pipeline is shutting down normally.
        self.out_queue.put(POISON)

class LastPipelineThread(Thread):
    """A thread running the last stage in a pipeline. The coroutine
    should yield nothing.
    """
    def __init__(self, coro, in_queue):
        super(LastPipelineThread, self).__init__()
        self.coro = coro
        self.in_queue = in_queue

    def run(self):
        # Prime the coroutine.
        next(self.coro)

        while True:
            # Get the message from the previous stage.
            msg = self.in_queue.get()
            #print( "final pipeline inq: ", msg )
            if msg is POISON:
                break
            elif isinstance(msg, PipelineError):
                self.exc = msg.exc
                return
            
            # Send to consumer.
            try:
                self.coro.send(msg)
            except Exception as exc:
                self.exc = exc
                return
        
        # No exception raised in pipeline.
        self.exc = None

class Pipeline(object):
    """Represents a staged pattern of work. Each stage in the pipeline
    is a coroutine that receives messages from the previous stage and
    yields messages to be sent to the next stage.
    """
    def __init__(self, stages):
        """Makes a new pipeline from a list of coroutines. There must
        be at least two stages.
        """
        if len(stages) < 2:
            raise ValueError('pipeline must have at least two stages')
        self.stages = stages
        
    def run_sequential(self):
        """Run the pipeline sequentially in the current thread. The
        stages are run one after the other.
        """
        # "Prime" the coroutines.
        for coro in self.stages[1:]:
            next(coro)
        
        # Begin the pipeline.
        for msg in self.stages[0]:
            for stage in self.stages[1:]:
                msg = stage.send(msg)
                if msg is BUBBLE:
                    # Don't continue to the next stage.
                    break
    
    def run_parallel(self, queue_size=DEFAULT_QUEUE_SIZE):
        """Run the pipeline in parallel using one thread per stage. The
        messages between the stages are stored in queues of the given
        size.
        """
        queues = [Queue(queue_size) for i in range(len(self.stages)-1)]
        threads = [FirstPipelineThread(self.stages[0], queues[0])]
        for i in range(1, len(self.stages)-1):
            threads.append(MiddlePipelineThread(
                self.stages[i], queues[i-1], queues[i]
            ))
        threads.append(LastPipelineThread(self.stages[-1], queues[-1]))
        
        # Start threads.
        for thread in threads:
            thread.start()
        
        # Wait for termination.
        try:
            for thread in threads:
                thread.join()
        except:
            # Shut down the pipeline by telling the first thread to
            # poison its channel.
            threads[0].abort()
            raise
        
        # Was there an exception?
        exc = threads[-1].exc
        if exc:
            raise exc

# Smoke test.
if __name__ == '__main__':

    import time
    import collections
    import os
    import mmap
    
    # def produce():
    #     for i in range(5):
    #         print( 'generating', i)
    #         time.sleep(1)
    #         yield i

    # def work():
    #     num = yield
    #     while True:
    #         print( 'processing', num)
    #         time.sleep(2)
    #         num = yield num*2

    # def consume():
    #     while True:
    #         num = yield
    #         time.sleep(1)
    #         print( 'received', num)


    a = '''this ''' #is a this is bytes bytes file file file to test bigram bigram counting.
        #for what it's worth worth here is some more tasty data.'''.split( )
    c = collections.Counter( )
    window_size = 2

    # f = open('../../SampleData/large_file.txt', 'r+b')
    # mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)


    f = open("../../SampleData/large_file.txt", "r")

    
    def read_mmap( ):
        buffer_size = 100000
        while True:
            buf = f.read(5)
            if not buf:
                print("breaking")
                break
            yield buf

            
    def tokenize( ):
        while True:
            text = (yield)
            text = text.split( )
            #print("producing tokens ", text)
            try:
                yield [(text[0], text[window_size])]
                del text[0]               
            except IndexError as e:
                pass #print(e)
                
    def count( ):
        while True:
            sg = (yield)
            #print("counting values", sg)
            c.update(sg)


    #ts_start = time.time()
    #Pipeline([produce(), work(), consume()]).run_sequential()
    #ts_middle = time.time()
    Pipeline([read_mmap( ), tokenize(), count()]).run_parallel()
    #ts_end = time.time()
    #print( 'Sequential time:', ts_middle - ts_start)

    print(c)
    #print( 'Parallel time:', ts_end - ts_middle)



        #     # if you read part way into a word, read some more until you hit a space
        # if buf[-1] != 32:
        #     extra = b""
        #     while True:
        #         extra_byte = mmap_file.read(1)
        #         if extra_byte:
        #             if extra_byte[0] != 32:
        #                 extra = extra + extra_byte
        #             else:
        #                 buf = buf + extra + extra_byte
        #                 break
        #         else:
        #             break
