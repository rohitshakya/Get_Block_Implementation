#  Used only in case of 'Delayed write' case. This allows asynchronous write on the disk.
import multiprocessing
import BufferHeader
import time
import os

def _writeAsynchronously(lock,bufferDataStructure,blockNumber):
    #locking as this is supposed to be a 
    #lock.acquire()

    print("************ Asynchronous Writing of Block number-",blockNumber," ***************")
    time.sleep(4)   #sleep for 4 seconds to simulate writing to disk
    
    bufferDataStructure.clearDelayedWriteBit(blockNumber)

    print("************ Asynchronous Writing of Block Number-",blockNumber," over ***************")
   
    #adding buffer to head of free list, to follow the LRU algorithm
    lock.acquire()
    bufferDataStructure.addToFreeListFirst(blockNumber)
    lock.release()


def asynchronousWrite(lock,bufferDataStructure,blockNumber):
    
    writingProcess=multiprocessing.Process(target=_writeAsynchronously,args=(lock,bufferDataStructure,blockNumber,))
    writingProcess.start()
    
    return 1
