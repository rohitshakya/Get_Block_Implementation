# This is our driver class. It imports multiprocessing package provided by python that supports spawning processes.
# It creates an object of BaseManager class so that the processes can access the shared objects by using proxy classes.

import random
import time
import os
import numpy as np
import multiprocessing
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Manager, Lock
from Queues import Queues
from CreateProcess import process
from SleepQueue import SleepQueue


noOfHashQ=int(input("number of HashQ: "))
flSize=int(input("freelist Size: ")) 
maxNoOfBlocks=int(input("maximum number of blocks: ")) 
processes=int(input("Number of Process to execute: ")) 

if __name__== '__main__':
    #Managers provide a way to create data which can be shared between different processes. A manager object controls a server process which 
    #manages shared objects 
    #BaseManager is used to create proxy classes in this session which are present in the shared memory
    # register is a class method which can be used for registering a type or callable with the manager class 
    BaseManager.register('Queues',Queues)
    BaseManager.register('SleepQueue',SleepQueue)

    manager=BaseManager()
    manager.start()

    sleepQueue=manager.SleepQueue()
    queues=manager.Queues(flSize,noOfHashQ)

    print("\nInitial State of hashQ")
    queues.printHashQ()
    print("\nInitial State of freeList")
    queues.printfl()

    lock=Lock()

    #Creating processes_array
    process_array=np.empty(processes,dtype=object)

    #initializing the elements in process array with processes from the multiprocessing class
    # In multiprocessing,processes are spawned by creating a Process object and then calling it's start() method 
    for i in range(processes):
        process_array[i]=Process(target=process,args=(sleepQueue,queues,lock,maxNoOfBlocks,))

    for i in range(processes):
        process_array[i].start()

    #waiting for processes to join (join- finish their operation and join this execution)

    for i in range(processes):
        process_array[i].join()

    #print when all the processes are finished
    print("\n~~~~~~~~~~~~~~ END ~~~~~~~~~~~~~~\n")
