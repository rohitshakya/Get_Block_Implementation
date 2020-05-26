import random                           #Randomint() returns a random integer between the specified integers.
import time                             #Used for sleep() function
import GetBlock
import os
import signal
noOfBufferRequestsByEachProcess=5


def pseudoOperation(queues ,buffer):
    """
    0-process went into long sleep while holding the buffer 
    1-work done(disk read is done if buffer was not initially valid), validate buffer 
    2-mark buffer invalid to simulate I/O error
    3-write operation followed by marking buffer delayed write block and validating block
    """
    queues.setValidBit(buffer)     # as after each bread the buffer is expected to be valid except for exceptions handled by operation 2
    time.sleep(2)                               #simulating an operation
    operation=random.randint(0,3)
    if(operation==0):
        print("Process ",os.getpid()," is going into long sleep with buffer ",buffer)
        time.sleep(15)
        print("Process ",os.getpid()," woke up from long sleep with buffer ",buffer)
    elif(operation==1):
        print("Operation 1 - Process ",os.getpid(), " Buffer: ",buffer)
        queues.setValidBit(buffer)
    elif(operation==2):
        print("Operation 2 - Process ",os.getpid(), " Buffer: ",buffer)        
        queues.clearValidBit(buffer)
    elif(operation==3):
        print("Operation 3 - Process ",os.getpid(), " Delayed Write: ",buffer)
        queues.setDelayedWriteBit(buffer)
        queues.setValidBit(buffer)
        


def pseudoBRelease(sleepQueue,queues,lock,buffer):
    
    lock.acquire()
    if(queues.isValid(buffer)):
        #adding the buffer to the tail of the freelist
        queues.addToflEnd(buffer)
    else:
        #adding the buffer to the head of the freelist(invalid data)
        queues.addToflFirst(buffer)

    #Unlock the buffer
    queues.clearLockedBit(buffer)
    
    print("Process ",os.getpid()," has unlocked buffer     ",buffer," Lock status:",queues.isLocked(buffer))
    print("freelist - Process ",os.getpid())
    queues.printfl()

   
    
    wakeAllProcessWaitingForAnyBuffer(sleepQueue)
    wakeAllProcessWaitingForBuffer(sleepQueue,buffer)
    lock.release()

def wakeAllProcessWaitingForBuffer(sleepQueue,buffer):
    #-2 is returned when no such entry for buffer in sleepQueue
    list=sleepQueue.getPidsWaitingForBuffer(buffer)
    if(list==-2):
        return
    for pid in list:
        #the current process will send the signal SIGINT to the process with process id =pid
        os.kill(pid,signal.SIGINT)


def wakeAllProcessWaitingForAnyBuffer(sleepQueue):
    #-2 is returned when no such entry for buffer in sleepQueue
    list=sleepQueue.getPidsWaitingForAnyBuffer()
    if(list==-2):
        return
    for pid in list:
        #the current process will send the signal SIGHUP to the process with process id =pid
        os.kill(pid,signal.SIGHUP)


def process(sleepQueue,queues,lock,maxNoOfBlocks):
    
    i=0
    while(i<noOfBufferRequestsByEachProcess):
        time.sleep(2) #process will request a random block after every 2 second
        requestedBlock=random.randint(0,maxNoOfBlocks-1)
        print("\n---------------------------------\nProcess ",os.getpid()," has requested block number ",requestedBlock,"\n---------------------------------\n")
        recievedBuffer=GetBlock.getBlock(sleepQueue,requestedBlock,lock,queues)
        print("\nProcess ",os.getpid(),": RECEIVED BUFFER => ",recievedBuffer)

        print("\n",os.getpid()," HashQ : ")
        queues.printHashQ()
        print("\n",os.getpid()," freelist :")
        queues.printfl()

        pseudoOperation(queues ,recievedBuffer)
        pseudoBRelease(sleepQueue,queues,lock,recievedBuffer)
        i+=1