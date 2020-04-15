import multiprocessing
import AsynchronousWrite
import time
import os
import BufferDataStructure
import signal
import SignalCatcher

#sleep function to make a process sleep for a particular buffer
def mySleepForBuffer(sleepQueue,buffer):
    signal.signal(signal.SIGINT,SignalCatcher.sigint_catcher)
    sleepQueue.add(buffer,os.getpid())
    signal.pause()#process will sleep till SIGINT signal is raised
    

#sleep function to make a process sleep for any buffer
def mySleepForAnyBuffer(sleepQueue):
    signal.signal(signal.SIGHUP,SignalCatcher.sighup_catcher)
    sleepQueue.add(-1,os.getpid()) #as processes waiting for any buffer state -1 as required buffer number
    signal.pause()#process will sleep till SIGHUP signal is raised
    


def getBlock(sleepQueue,blockNumber,lock,bufferDataStructure):
    bufferFound=False
    while (not bufferFound):

        lock.acquire()     #lock

        #1. The buffer is in the hashQ 
        if (bufferDataStructure.isPresentInHashQ(blockNumber)):
            #buffer=hashQ.findBlockInHashQ(blockNumber)
            if(bufferDataStructure.isLocked(blockNumber)):

                #For revealing the scenario under which process is going to sleep
                print("Process ",os.getpid()," is going to sleep as buffer ",blockNumber," is present in hashQ and is busy")
                lock.release()
                # time.sleep(4)
                mySleepForBuffer(sleepQueue,blockNumber)
                continue
            
            #Reqiured buffer is in the hash queue and unlocked
            bufferDataStructure.setLockedBit(blockNumber)
            bufferDataStructure.removeFromFreeList(blockNumber)

            #Return the buffer to the requesting process
            print("Process ",os.getpid()," will get buffer ",blockNumber," from hashQ")
            bufferFound=True
            lock.release()
            return blockNumber

        #2. Buffer is not in the hashQ. Hence, check freelist for the buffer  
        else:
            #Freelist is empty
            if (bufferDataStructure.isEmptyFreeList()):   

                #For revealing the scenario under which process is going to sleep
                print("Process ",os.getpid()," is going to sleep as freeList is empty")

                lock.release()
                mySleepForAnyBuffer(sleepQueue) 
                continue

            #Freelist is not empty
            blockNumber_freeList=bufferDataStructure.getAnyFromFreeList() #just getting the first free buffer(not removing from free list yet)

            #Check if the buffer is marked as 'delayed write'
            if(bufferDataStructure.isDelayedWrite(blockNumber_freeList)):

                #Now removing it from free list
                bufferDataStructure.removeFromFreeList(blockNumber_freeList)
                print("freelist after removing ",blockNumber_freeList)
                bufferDataStructure.printFreeList()
                #For revealing the scenario under which process is going to do asynchronous write
                print("Process ",os.getpid()," came across free buffer ",blockNumber_freeList, " but marked as delayed write so is executing asynchronous write")
                
                lock.release()
                AsynchronousWrite.asynchronousWrite(lock,bufferDataStructure,blockNumber_freeList)
                continue

            #Found a free buffer in the freelist 
            bufferDataStructure.removeFromHashQ(blockNumber_freeList)

            print("Replace buffer ",blockNumber_freeList," in freeList, with buffer ",blockNumber)


            print("Buffer ",blockNumber_freeList," is removed from free list")
            print("Buffer ",blockNumber," added to the hash queue")
            #replacing the old block number(returnrd from the freeList ) with the new block number
            bufferDataStructure.setBlockNumber(blockNumber_freeList,blockNumber)
            

            #Add buffer to the new hash queue
            bufferDataStructure.addBlockToHashQ(blockNumber)

            #remove it from the free list
            bufferDataStructure.removeFromFreeList(blockNumber) 

            #Update status of the buffer
            bufferDataStructure.setLockedBit(blockNumber)
            bufferDataStructure.clearValidBit(blockNumber)


            bufferFound=True
            lock.release()
            return blockNumber





