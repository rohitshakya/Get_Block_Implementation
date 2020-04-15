class BufferHeader(object):
    
    def __init__(self,blockNumber=None):
        
        if(blockNumber==None):
            self.block_number=0       #valid block numbers are from 0 onwards
        else:
            self.block_number=blockNumber

        self.status_locked=0
        self.status_valid=0
        self.status_delayed_write=0
        self.waiting_process_count=0

        self.hashQ_next=self
        self.hashQ_prev=self
        self.freeList_next=None
        self.freeList_prev=None


    # block number manipulation
    def setBlockNumber(self,block_number):
        self.block_number=block_number

    def getBlockNumber(self):
        return self.block_number


    #status manipulation
    def setLockedBit(self):
        self.status_locked=1

    def clearLockedBit(self):
        self.status_locked=0

    def isLocked(self):
        if(self.status_locked==1):
            return True
        return False

    #Valid Bit Manipulation
    def setValidBit(self):
        self.status_valid=1
    
    def clearValidBit(self):
        self.status_valid=0

    def isValid(self):
        if(self.status_valid==1):
            return True
        return False 

    #Delayed Write Bit Manipulation
    def setDelayedWriteBit(self):
        self.status_delayed_write =1
    
    def clearDelayedWriteBit(self):
        self.status_delayed_write =0

    def isDelayedWrite(self):
        if(self.status_delayed_write ==1):
            return True
        return False 


    # Waiting Process manipulation
    def addWaitingProcess(self):
        self.waiting_process_count= self.waiting_process_count+ 1
    
    def removeWaitingProcess (self):
        if (self.waiting_process_count==0):
            return -1
        self.status_delayed_write = self.waiting_process_count- 1

    def hasWaitingProcess (self):
        if(self.waiting_process_count >0):
            return True
        return False 



    #hashQ manipulation

    #next

    def getNextHashQ(self):
        return self.hashQ_next

    def addNextHashQ(self,next):
        if(isinstance(next,BufferHeader)):
            self.hashQ_next=next
            return 1
        else:
             return 0

    def removeNextHashQ(self):
        self.hashQ_next=None

    #prev    

    def getPrevHashQ(self):
        return self.hashQ_prev

    def addPrevHashQ(self,prev):
        if(isinstance(prev,BufferHeader) ):
            self.hashQ_prev=prev
            return 1
        else:
            return 0

    def removePrevHashQ(self):
        self.hashQ_prev=None


    #freeList manipulation

    #next

    def getNextFreeList(self):
        return self.freeList_next

    def addNextFreeList(self,next):
        self.status_locked=0
        if(isinstance(next,BufferHeader)):
            self.freeList_next=next
            return 1
        else :
            return 0

    def removeNextFreeList(self):
        self.freeList_next=None

    #prev

    def getPrevFreeList(self):
        return self.freeList_prev

    def addPrevFreeList(self,prev):
        self.status_locked=0
        if(isinstance(prev,BufferHeader)):
            self.freeList_prev=prev
            return 1
        else :
            return 0

    def removePrevFreeList(self):
        self.freeList_prev=None
        