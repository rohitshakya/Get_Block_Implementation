import random
import BufferHeader
import multiprocessing
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Manager
import random
import time
import BufferDataStructure
import BufferHeader
import BufferManagement
import os
import myProcess
import SleepQueue
import numpy as np



noOfHashQ=4
freeListSize=20
maxNoOfBlocks=30
noOfProcesses=5
if __name__== '__main__':
    #using shared memory objects using BaseManager from multiprocessing library
    #BaseManager is used to create proxy classes in this session which are present in the shared memory
    BaseManager.register('BufferDataStructure',BufferDataStructure.BufferDataStructure)
    BaseManager.register('SleepQueue',SleepQueue.SleepQueue)

    manager=BaseManager()
    manager.start()

    sleepQueue=manager.SleepQueue()
    bufferDataSructure=manager.BufferDataStructure(freeListSize,noOfHashQ)

    print("\nInitial State of hashQ")
    bufferDataSructure.printHashQ()
    print("\nInitial State of freeList")
    bufferDataSructure.printFreeList()

    lock=multiprocessing.Lock()


    #Creating processes_array
    process_array=np.empty(noOfProcesses,dtype=object)

    #initializing the elements in process array with procvesses from the multiprocessing class

    for i in range(noOfProcesses):
        process_array[i]=Process(target=myProcess.process,args=(sleepQueue,bufferDataSructure,lock,maxNoOfBlocks,))

    for i in range(noOfProcesses):
        process_array[i].start()

        

    #waiting for processes to join (join- finish their operation and join this execution)

    for i in range(noOfProcesses):
        process_array[i].join()

    #print when all the processes are finished
    print("\n~~~~~~~~~~~~~~ END ~~~~~~~~~~~~~~\n")






