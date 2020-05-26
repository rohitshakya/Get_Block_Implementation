import multiprocessing #threading interface
import time #sleep()
import os
import signal
import multiprocessing
import Header


def _writeAsynchronously(lock,queues,blockNumber):

    print("************ Asynchronous Writing of Block number-",blockNumber," ***************")
    time.sleep(8)   #sleep for 4 seconds to simulate writing to disk
    
    queues.clearDelayedWriteBit(blockNumber)

    print("************ Asynchronous Writing of Block Number-",blockNumber," Completed ***************")
   
    #adding buffer to head of free list, to follow the LRU algorithm
    lock.acquire()
    queues.addToflFirst(blockNumber)
    lock.release()


def asynchronousWrite(lock,queues,blockNumber):
    writingProcess=multiprocessing.Process(target=_writeAsynchronously,args=(lock,queues,blockNumber,))
    writingProcess.start()
    
    return 1


# These functions are called by the target environment when the corresponding signal occurs.
# The target environment suspends execution of the program until the signal catcher returns.

# This function generates signal for processes waiting for a particular buffer
def sigint_catcher(sig,frame):
    print("process: ",os.getpid()," woke up as it was sleeping for a particular buffer" )

#It generates the signal for processes waiting for any buffer
def sighup_catcher(sig,frame):
    print("process: ",os.getpid()," woke up as it was sleeping for a any buffer" )

#  Used only in case of 'Delayed write' case. This allows asynchronous write on the disk.

#sleep function to make a process sleep for a particular buffer
def mySleepForBuffer(sleepQueue,buffer):
    signal.signal(signal.SIGINT,sigint_catcher)
    sleepQueue.add(buffer,os.getpid())
    signal.pause()#process will sleep till SIGINT signal is raised
    

#sleep function to make a process sleep for any buffer
def mySleepForAnyBuffer(sleepQueue):
    signal.signal(signal.SIGHUP,sighup_catcher)
    sleepQueue.add(-1,os.getpid()) #as processes waiting for any buffer state -1 as required buffer number
    signal.pause()#process will sleep till SIGHUP signal is raised
    


def getBlock(sleepQueue,blockNumber,lock,queues):
    bufferFound=False
    while (not bufferFound):

        lock.acquire()     #lock

        #The buffer is in the hashQ 
        if (queues.isPresentInHashQ(blockNumber)):
            #5 The Buffer is found in the hashQ, but its buffer currently busy. So, the process going to sleep
            if(queues.isLocked(blockNumber)):
                print("Process ",os.getpid()," is going to sleep as buffer ",blockNumber," is present in hashQ and is busy")
                #releasing the Upper acquired lock and continue for next process
                lock.release() #5 release
                mySleepForBuffer(sleepQueue,blockNumber)
                continue
            
            #1. Reqiured buffer is in the hash queue and Free
            queues.setLockedBit(blockNumber)
            queues.removeFromfl(blockNumber)

            #Return the buffer to the requesting process
            print("Process ",os.getpid()," will get buffer ",blockNumber," from hashQ")
            bufferFound=True
            lock.release() #1 release
            return blockNumber

        #Buffer is not in the hashQ. Hence, check freelist for the buffer  
        else:
            #4. freelist is empty i.e there is no buffer to use. So, process going to sleep.
            if (queues.isEmptyfl()):
                print("Process ",os.getpid()," is going to sleep as freelists is empty")

                lock.release() #4 release
                mySleepForAnyBuffer(sleepQueue) 
                continue

            #2. freelist is not empty and just getting the first free buffer available
            blockNumber_fl=queues.getAnyFromfl()

            #3. Check if the buffer is marked as 'delayed write'
            if(queues.isDelayedWrite(blockNumber_fl)):

                #Now removing it from free list
                queues.removeFromfl(blockNumber_fl)
                print("freelist after removing ",blockNumber_fl)
                queues.printfl()
                #For revealing the scenario under which process is going to do asynchronous write
                print("Process ",os.getpid()," came across free buffer ",blockNumber_fl, " but marked as delayed write so is executing asynchronous write")
                
                lock.release() #3 release
                asynchronousWrite(lock,queues,blockNumber_fl)
                continue

            #Found a free buffer in the freelist 
            queues.removeFromHashQ(blockNumber_fl)

            print("Replace buffer ",blockNumber_fl," in freelist, with buffer ",blockNumber)


            print("Buffer ",blockNumber_fl," is removed from free list")
            print("Buffer ",blockNumber," added to the hash queue")
            #replacing the old block number(returnrd from the freelist ) with the new block number
            queues.setBlockNumber(blockNumber_fl,blockNumber)
            

            #Add buffer to the new hash queue
            queues.addBlockToHashQ(blockNumber)

            #remove it from the free list
            queues.removeFromfl(blockNumber) 

            #Update status of the buffer
            queues.setLockedBit(blockNumber)
            queues.clearValidBit(blockNumber)


            bufferFound=True
            lock.release() #2 release
            return blockNumber

