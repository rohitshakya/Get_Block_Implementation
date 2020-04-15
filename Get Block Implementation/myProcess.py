import random
import time
import multiprocessing
import BufferDataStructure
import BufferHeader
import BufferManagement
import os
import signal

noOfBufferRequestsByEachProcess=5


def pseudoOperation(bufferDataStructure ,buffer):
    #print("operation by process: ",os.getpid()," on buffer: ",buffer)
    """
    0-write operation followed by marking buffer delayed write block and validating block 
    1-work done(disk read is done if buffer was not initially valid), validate buffer 
    2-mark buffer invalid to simulate I/O error
    3-process went into long sleep while holding the buffer
    """
    bufferDataStructure.setValidBit(buffer) # as after each bread the buffer is expected to be valid except for exceptions handled by operation 2
    time.sleep(2) #simulating an operation
    operation=random.randint(0,3)
    if(operation==0):
        print("Operation 0 - Process ",os.getpid(), " Delayed Write: ",buffer)
        bufferDataStructure.setDelayedWriteBit(buffer)
        bufferDataStructure.setValidBit(buffer)
    elif(operation==1):
        print("Operation 1 - Process ",os.getpid(), " Buffer: ",buffer)
        bufferDataStructure.setValidBit(buffer)
    elif(operation==2):
        print("Operation 2 - Process ",os.getpid(), " Buffer: ",buffer)        
        bufferDataStructure.clearValidBit(buffer)
    elif(operation==3):
        print("Process ",os.getpid()," is going into long sleep with buffer ",buffer)
        time.sleep(15)
        print("Process ",os.getpid()," woke up from long sleep with buffer ",buffer)


def pseudoBRelease(sleepQueue,bufferDataStructure,lock,buffer):
    
    lock.acquire()
    #print("brelease by process: ",os.getpid()," on buffer: ",buffer)
    if(bufferDataStructure.isValid(buffer)):
        #adding the buffer to the tail of the freelist
        bufferDataStructure.addToFreeListEnd(buffer)
    else:
        #adding the buffer to the head of the freelist(invalid data)
        bufferDataStructure.addToFreeListFirst(buffer)

    #Unlock the buffer
    bufferDataStructure.clearLockedBit(buffer)
    
    print("Process ",os.getpid()," has unlocked buffer ",buffer,"            Lock status:",bufferDataStructure.isLocked(buffer))
    print("FreeList - Process ",os.getpid())
    bufferDataStructure.printFreeList()

   
    
    wakeAllProcessWaitingForAnyBuffer(sleepQueue)
    wakeAllProcessWaitingForBuffer(sleepQueue,buffer)
    lock.release()

def wakeAllProcessWaitingForBuffer(sleepQueue,buffer):
    #-2 is returned when no such entry for buffer in sleepQueue
    list=sleepQueue.getPidsWaitingForBuffer(buffer)
    if(list==-2):
        return
    for pid in list:
        os.kill(pid,signal.SIGINT)


def wakeAllProcessWaitingForAnyBuffer(sleepQueue):
    #-2 is returned when no such entry for buffer in sleepQueue
    list=sleepQueue.getPidsWaitingForAnyBuffer()
    if(list==-2):
        return
    for pid in list:
        os.kill(pid,signal.SIGHUP)


def process(sleepQueue,bufferDataStructure,lock,maxNoOfBlocks):
    
    i=0
    while(i<noOfBufferRequestsByEachProcess):
        time.sleep(2) #process will request a random block after every 2 second
        requestedBlock=random.randint(0,maxNoOfBlocks-1)
        print("\n---------------------------------------------------------\nProcess ",os.getpid()," has requested block number ",requestedBlock,"\n---------------------------------------------------------\n")
        recievedBuffer=BufferManagement.getBlock(sleepQueue,requestedBlock,lock,bufferDataStructure)
        print("\nProcess ",os.getpid(),": RECIEVED BUFFER ",recievedBuffer)

        print("\n",os.getpid()," HashQ : ")
        bufferDataStructure.printHashQ()
        print("\n",os.getpid()," FreeList :")
        bufferDataStructure.printFreeList()

        
        pseudoOperation(bufferDataStructure ,recievedBuffer)
        pseudoBRelease(sleepQueue,bufferDataStructure,lock,recievedBuffer)
        i+=1

        




