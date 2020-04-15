import BufferHeader

class BufferDataStructure(object):

    def __init__(self, freeListSize=20, hashQSize=4):
        
        """
        FREE LIST PART
        """
        # what's the meaning of this simulation if the freelistsize is smaller than 1. LOL
        if(freeListSize < 1):
            return
        self.freeListSize = freeListSize
        #adding BufferHeader class type to manager and using this so that it can be shared among processes
        self.freeListHeader = BufferHeader.BufferHeader(-1)

        prevBlock = self.freeListHeader

        # implementing the (circular doubly linked) free list
        for i in range(1, self.freeListSize):
            block = BufferHeader.BufferHeader(-1)
            prevBlock.addNextFreeList(block)
            block.addPrevFreeList(prevBlock)
            prevBlock = block

        prevBlock.addNextFreeList(self.freeListHeader)
        self.freeListHeader.addPrevFreeList(prevBlock)

        """
        END OF FREE LIST PART
        """

        """
        HASH QUEUE PART
        """
        self.hashQSize=hashQSize
        self.hashQ=[]
        #creating 4 empty hashQ
        for i in range(self.hashQSize):
            self.hashQ.append(None)

        """
        END OF HASH QUEUE PART
        """    

    def mapFreeListIntoHashQ(self):
        block=self.freeListHeader
        for i in range(self.freeListSize):
            self.addBlockToHashQ(block.getBlockNumber())
            block=block.getNextFreeList()


    def getHeader(self):
        return self.freeListHeader

    def findInFreeList(self,blockNumber):
        buffer=self.freeListHeader
        if(buffer.getBlockNumber()==blockNumber):
            return buffer
        
        buffer=buffer.getNextFreeList()
        
        while(buffer!=self.freeListHeader):
            
            if(buffer.getBlockNumber()==blockNumber):
                return buffer
            buffer=buffer.getNextFreeList()

        return None

    def isEmptyFreeList(self):
        if (self.freeListHeader==None):
            return True
        return False

    # adding a buffer to the tail of the freelist 
    def addToFreeListEnd(self, blockNumber):

        #if being added to free list then it means it is in hashQ
        block=self.findBlockInHashQ(blockNumber)


        #adding a buffer to the empty freelist
        if(self.freeListHeader == None):
            self.freeListHeader = block
            block.addNextFreeList(block)
            block.addPrevFreeList(block)
            return
        lastBlock = self.freeListHeader.getPrevFreeList()

        lastBlock.addNextFreeList(block)
        block.addPrevFreeList(lastBlock)

        block.addNextFreeList(self.freeListHeader)
        self.freeListHeader.addPrevFreeList(block)

    # adding a buffer to the head of the freelist (in special cases)
    def addToFreeListFirst(self, blockNumber):

        #if being added to free list then it means it is in hashQ
        block=self.findBlockInHashQ(blockNumber)

        #adding a buffer to the empty freelist
        if(self.freeListHeader == None):
            self.freeListHeader = block
            block.addNextFreeList(block)
            block.addPrevFreeList(block)
            return
        lastBlock = self.freeListHeader.getPrevFreeList()

        lastBlock.addNextFreeList(block)
        block.addPrevFreeList(lastBlock)

        block.addNextFreeList(self.freeListHeader)
        self.freeListHeader.addPrevFreeList(block)

        # only change in add to first from adding to end as it is a circular Queue
        self.freeListHeader = block

    def getAnyFromFreeList(self):
        if(self.isEmptyFreeList()):
            return -1
        block=self.freeListHeader
        #self.removeFromFreeList(block.getBlockNumber())
        return block.getBlockNumber() #block.getBlockNumber()

    def removeFromFreeList(self, blockNumber):

        block=self.findBlockInHashQ(blockNumber)
        # validating if block in free list
        if(block.getPrevFreeList() == None or block.getNextFreeList() == None):
            return -1  # nothing is removed
        
        # only single element and that is the block that will be removed
        if (self.freeListHeader.getNextFreeList() == self.freeListHeader and self.freeListHeader == block):
            block.removeNextFreeList()
            block.removePrevFreeList()
            self.freeListHeader = None
            return block.getBlockNumber()  # successfully removed
        # if block to be remove is the header then shift heaader to next place then follow the same cource of action
        elif (self.freeListHeader == block):
            self.freeListHeader = block.getNextFreeList()

        # altering freelist links
        block.getPrevFreeList().addNextFreeList(block.getNextFreeList())
        block.getNextFreeList().addPrevFreeList(block.getPrevFreeList())

        # removing links from present block
        block.removeNextFreeList()
        block.removePrevFreeList()
        #print("Buffer ",block.getBlockNumber(), " removed from free list ")
        return block.getBlockNumber()

    def printFreeList(self):
        block = self.freeListHeader
        if(block==None):
            print("FreeList is Empty")
        while(block!=None):
            print("<-", block.getBlockNumber(), "->", end="")
            block = block.getNextFreeList()
            if(block == self.freeListHeader):
                break
        print()






    """
    HASH QUEUE MANIPULATION
    """

    def findBlockInHashQ(self, blockNumber ):
        # queue = blocknum MOD 4
        queue=possibleBlock=self.hashQ[blockNumber%self.hashQSize] #possible queue
        while(queue!=None):
            if(possibleBlock.getBlockNumber()==blockNumber):
                return possibleBlock #block is found

            possibleBlock=possibleBlock.getNextHashQ()
            
            if(possibleBlock==queue):
                break

        return None

    def isPresentInHashQ(self,blockNumber):
        if(self.findBlockInHashQ(blockNumber)!=None):
            return True
        return False


    def addBlockToHashQ(self,blockNumber):
        block=self.findInFreeList(blockNumber)
        
        if(block==None):
            block=BufferHeader.BufferHeader(blockNumber)
        queueStart=self.hashQ[block.getBlockNumber() %self.hashQSize] #queue to which the block has to be added 
    
        #print("Buffer ",block.getBlockNumber()," added to the hash queue")
        #if queue is empty
        if (queueStart==None):
            
            self.hashQ[block.getBlockNumber() %self.hashQSize]=block
            block.addNextHashQ(block)
            block.addPrevHashQ(block)
            return 1            ##success
        queueEnd=queueStart.getPrevHashQ()

        queueEnd.addNextHashQ(block)
        block.addPrevHashQ(queueEnd)

        block.addNextHashQ(queueStart)
        queueStart.addPrevHashQ(block)
            
        return 1

    def removeFromHashQ(self,blockNumber):
        block=self.findBlockInHashQ(blockNumber)
        if(block==None):
           return -1


     
        if(block.getNextHashQ()==None and block.getPrevHashQ()==None):#block not in hashQ(starting cases)
            
            return 1
        if(block.getNextHashQ()==block ):#only one element in hashQ
            
            block.removeNextHashQ()
            block.removePrevHashQ()
            self.hashQ[block.getBlockNumber()%self.hashQSize]=None
            return 1
            
        
        if(self.hashQ[block.getBlockNumber()%self.hashQSize].getBlockNumber()==block.getBlockNumber()):#when the element to be removed is first element of the queue
            
            self.hashQ[block.getBlockNumber()%self.hashQSize]=block.getNextHashQ()
        block.getPrevHashQ().addNextHashQ(block.getNextHashQ())
        block.getNextHashQ().addPrevHashQ(block.getPrevHashQ())


    def printHashQ(self):
        for i in range(self.hashQSize ):
            block=self.hashQ[i]
            if(block==None):
                print("Empty\n")
                continue

            while(True):
                print("<-",block.getBlockNumber(),"->" ,end="")
                block=block.getNextHashQ()
                if(block==self.hashQ[i]):
                    break
            
            print("\n")



    '''
    Code for block manipulation through this memory pool
    '''

    #block number manipulation
    def setBlockNumber(self,oldBlockNumber,newBlockNumber):
        buffer=self.findBlockInHashQ(oldBlockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(oldBlockNumber)
        buffer.setBlockNumber(newBlockNumber)




    #status manipulation

    def setLockedBit(self,blockNumber):
        buffer=self.findBlockInHashQ(blockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(blockNumber)
        buffer.setLockedBit()

    def clearLockedBit(self,blockNumber):
        buffer=self.findBlockInHashQ(blockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(blockNumber)
        buffer.clearLockedBit()

    def isLocked(self,blockNumber):
        buffer=self.findBlockInHashQ(blockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(blockNumber)
        return buffer.isLocked()



    
    def setValidBit(self,blockNumber):
        buffer=self.findBlockInHashQ(blockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(blockNumber)
        buffer.setValidBit()
    
    def clearValidBit(self,blockNumber):
        buffer=self.findBlockInHashQ(blockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(blockNumber)
        buffer.clearValidBit()

    def isValid(self,blockNumber):
        buffer=self.findBlockInHashQ(blockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(blockNumber)
        return buffer.isValid()
        



    def setDelayedWriteBit(self,blockNumber):
        buffer=self.findBlockInHashQ(blockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(blockNumber)
        buffer.setDelayedWriteBit()
    
    def clearDelayedWriteBit(self,blockNumber):
        buffer=self.findBlockInHashQ(blockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(blockNumber)
        buffer.clearDelayedWriteBit()

    def isDelayedWrite(self,blockNumber):
        buffer=self.findBlockInHashQ(blockNumber)
        if(buffer==None):
            buffer=self.findInFreeList(blockNumber)
        return buffer.isDelayedWrite()

