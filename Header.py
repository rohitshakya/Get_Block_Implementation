"""
The buffer is the in- memory copy of the disk block.
Buffer consists of two parts: a memory array that contains data from disk and a buffer header that identifies the buffer.
The buffer header contains a device number field and a block number field that specify the file system and block number of the data on disk and uniquely identify the buffer.
"""
from random import randint

class Header(object):
    
    def __init__(self,blockNumber=None):
        self.block_number=blockNumber       #block_number is the block number of data on the disk
        self.locked=0                #locked indicates whether the buffer is currently locked or not
        self.valid=0                 #valid indicates whether the buffer contains valid data or not
        self.delayed_write=0         #delayed_write indicates whether the kernel must write buffer contents to disk before reassigning the buffer or not
        self.waiting_process_count=0        #waiting_process_count specifies number of processes waiting for the buffer to become free
        self.hashQ_next=None                #pointer to next buffer on hash queue
        self.hashQ_prev=None                #pointer to previous buffer on hash queue
        self.fl_next=None             #pointer to next buffer on free list
        self.fl_prev=None             #pointer to previous buffer on free list

    # block number manipulation
    def setBlockNumber(self,block_number):
        self.block_number=block_number
    # returns block number of the buffer
    def getBlockNumber(self):
        return self.block_number

    # signifies that buffer is busy
    def setLockedBit(self):
        self.locked=1
    # signifies that buffer is free
    def clearLockedBit(self):
        self.locked=0
    # checks whether the buffer is free or not
    def isLocked(self):
        if(self.locked==1):
            return True
        return False

    # signifies that buffer contains valid data
    def setValidBit(self):
        self.valid=1
    # signifies that buffer doesn't contain valid data
    def clearValidBit(self):
        self.valid=0
    # checks whether the buffer contains valid data or not
    def isValid(self):
        if(self.valid==1):
            return True
        return False 

    # sets the delayed_write attribute signifying that buffer contenets have yet to be written on disk by the kernel
    def setDelayedWriteBit(self):
        self.delayed_write =1
    # clears the delayed_write attribute signifying that asynchronous write has completed
    def clearDelayedWriteBit(self):
        self.delayed_write =0
    # checks whether the delayed_write attribute is set or not
    def isDelayedWrite(self):
        if(self.delayed_write ==1):
            return True
        return False 

    '''
    # increments the count of waiting processes for thr buffer to become free
    def addWaitingProcess(self):
        self.waiting_process_count= self.waiting_process_count+ 1
    # decrements the count of waiting processes and returns -1 if no process is waiting for buffer
    def removeWaitingProcess (self):
        if (self.waiting_process_count==0):
            return -1
        self.delayed_write = self.waiting_process_count- 1
        # checks whether buffer has any process waiting for it
    def hasWaitingProcess (self):
        if(self.waiting_process_count >0):
            return True
        return False '''


    # returns next buffer of the hash queue for the buffer which called the method
    def getNextHashQ(self):
        return self.hashQ_next
    # adds next buffer on the hash queue for the buffer which called the method
    def addNextHashQ(self,next):
        if(isinstance(next,Header)):
            self.hashQ_next=next
            return 1
        else:
             return 0
    # removes next buffer on the hash queue for the buffer which called the method
    def removeNextHashQ(self):
        self.hashQ_next=None

    # returns previous buffer on the hash queue for the buffer which called the method
    def getPrevHashQ(self):
        return self.hashQ_prev
    # adds previous buffer on the hash queue for the buffer which called the method
    def addPrevHashQ(self,prev):
        if(isinstance(prev,Header) ):
            self.hashQ_prev=prev
            return 1
        else:
            return 0
    # remove previous buffer on the hash queue for the buffer which called the method
    def removePrevHashQ(self):
        self.hashQ_prev=None

    # returns next buffer on the free list for the buffer which called the method
    def getNextfl(self):
        return self.fl_next
    # adds next buffer on the free list for the buffer which called the method
    def addNextfl(self,next):
        self.locked=0
        if(isinstance(next,Header)):
            self.fl_next=next
            return 1
        else :
            return 0
    # removes next buffer on the free list for the buffer which called the method
    def removeNextfl(self):
        self.fl_next=None

    # returns previous buffer on the free list for the buffer which called the method
    def getPrevfl(self):
        return self.fl_prev

    # adds previous buffer on the free list for the buffer which called the method
    def addPrevfl(self,prev):
        self.locked=0
        if(isinstance(prev,Header)):
            self.fl_prev=prev
            return 1
        else :
            return 0

    # removes previous buffer on the free list for the buffer which called the method
    def removePrevfl(self):
        self.fl_prev=None
        