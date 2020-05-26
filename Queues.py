"""
fl: The free list is a doubly linked circular list of buffers. Buffers are added in the free list according to least recenty used(LRU) algorithm.
Hash queue: Buffers are organized in separate queues, hashed as a function of the device number and block number. we have considered only block number while hashing them.
"""
import Header
# since we are importing Buffer file in shared Queues file, Buffer will
# also be shared


class Queues(object):

    def __init__(self, noOfBuffers, hashQSize):
       
        if(noOfBuffers < 1):
            print("fl size cannot be less than 1.")
            return
        self.noOfBuffers = noOfBuffers
        # creating freelist header
        self.flHeader = Header.Header(-1)

        firstBlock = self.getflHeader()

        # implementing the (circular doubly linked) free list
        for i in range(1, self.noOfBuffers):
            block = Header.Header(-1)
            firstBlock.addNextfl(block)
            block.addPrevfl(firstBlock)
            firstBlock = block

        firstBlock.addNextfl(self.getflHeader())
        self.getflHeader().addPrevfl(firstBlock)

        self.hashQSize=hashQSize
        self.hashQ=[]
        #creating 4 empty hashQ
        for i in range(self.hashQSize):
            self.hashQ.append(None)
 


    def getflHeader(self):
        return self.flHeader
        
    # returns a b1 with block number == blockNumber from the freelist but does not remove it
    def findInfl(self,blockNumber):
        b1=self.getflHeader()
        if(b1.getBlockNumber()==blockNumber):
            return b1
        
        b1=b1.getNextfl()
        while(b1!=self.getflHeader()):
            if(b1.getBlockNumber()==blockNumber):
                return b1
            b1=b1.getNextfl()
        return None
        
        
    # checks whether freelist is empty or not
    def isEmptyfl(self):
        if (self.getflHeader()==None):
            return True
        return False

    # adding a b1 to the tail of the freelist 
    def addToflEnd(self, blockNumber):

        #if being added to free list then it means it is in hashQ
        block=self.findBlockInHashQ(blockNumber)


      # If freelist is empty, then the b1 being added will be the only element in the list
        if(self.getflHeader() == None):
            self.flHeader = block
            block.addNextfl(block)
            block.addPrevfl(block)
            return
        bn = self.getflHeader().getPrevfl()

        bn.addNextfl(block)
        block.addPrevfl(bn)

        block.addNextfl(self.getflHeader())
        self.getflHeader().addPrevfl(block)

    # adding a b1 to the head of the freelist (in special cases)
    def addToflFirst(self, blockNumber):

        #if being added to free list then it means it is in hashQ
        block=self.findBlockInHashQ(blockNumber)
        # If a b1 is being added in the starting of the free list, then it means earlier it was on hash queue and
        # could be a delayed_write b1 or some I/O error might have occurred
        if(self.getflHeader() == None):
            self.flHeader = block
            block.addNextfl(block)
            block.addPrevfl(block)
            return
        bn = self.getflHeader().getPrevfl()

        bn.addNextfl(block)
        block.addPrevfl(bn)

        block.addNextfl(self.getflHeader())
        self.getflHeader().addPrevfl(block)

        # only change in add to first from adding to end as it is a circular Queue
        self.flHeader = block
        
    # removes first free b1 from the free list
    def getAnyFromfl(self):
        if(self.isEmptyfl()):
            return -1
        block=self.getflHeader()
        return block.getBlockNumber() 
        
    # removes b1 with block number = blockNumber from free list
    def removeFromfl(self, blockNumber):

        block=self.findBlockInHashQ(blockNumber)
        
        # only single element and that is the block that will be removed
        if(block.getPrevfl() == None or block.getNextfl() == None):
            return -1  # nothing is removed
        
        # only single element and that is the block that will be removed
        if (self.getflHeader().getNextfl() == self.getflHeader() and self.getflHeader() == block):
            block.removeNextfl()
            block.removePrevfl()
            self.flHeader = None
            return block.getBlockNumber()  # successfully removed
        # if block to be remove is the header then shift heaader to next place then follow the same cource of action
        elif (self.getflHeader() == block):
            self.flHeader = block.getNextfl()

        # altering freelist links
        block.getPrevfl().addNextfl(block.getNextfl())
        block.getNextfl().addPrevfl(block.getPrevfl())

        # removing links from present block
        block.removeNextfl() 
        block.removePrevfl()
        return block.getBlockNumber()

	# prints contents of freelist
    def printfl(self):
        block = self.getflHeader()
        if(block==None):
            print("freelist is Empty")
        while(block!=None):
            print("[ blkno: ", block.getBlockNumber(), " ]",end="=>")
            block = block.getNextfl()
            if(block == self.getflHeader()):
                break
            
        print("\n")

    def findBlockInHashQ(self, blockNumber ):
        q=b1=self.hashQ[blockNumber%self.hashQSize] #possible queue
        while(q is not None):
            if(b1.getBlockNumber()==blockNumber):
                return b1 #block is found

            b1=b1.getNextHashQ()
            # first b1 again
            if(b1==q):
                break

        return None

    # first function to be invoked when in getblk algo to distinguish cases 1 and 5 with  2, 3 and 4
    # returns true if b1 with mentioned block number is found in hash queue which is being checked by calling findBlockInhashQueue()
    def isPresentInHashQ(self,blockNumber):
        if(self.findBlockInHashQ(blockNumber) is not None):
            return True
        return False

    # Called when required b1 is not in the hash queue and freelist is not empty
    def addBlockToHashQ(self,blockNumber):
        block=self.findInfl(blockNumber)
        
        if(block==None):
            block=Header.BufferHeader(blockNumber)
        b1=self.hashQ[block.getBlockNumber() %self.hashQSize] #queue to which the block has to be added 
    
        #if queue is empty
        if (b1==None):
            
            self.hashQ[block.getBlockNumber() %self.hashQSize]=block
            block.addNextHashQ(block)
            block.addPrevHashQ(block)
            return 1            ##success
        bn=b1.getPrevHashQ()

        bn.addNextHashQ(block)
        block.addPrevHashQ(bn)

        block.addNextHashQ(b1)
        b1.addPrevHashQ(block)
            
        return 1

    # Will be called when CASE-2 occurs and iff b1 in freelist contains a valid block number
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
                print(" Hash Queue [", i, "] is empty\n")
                continue
            print("HashQueue:",i)

            while(True):
                print("[ blkno: ", block.getBlockNumber(), " ]", end="=>")
                block=block.getNextHashQ()
                if(block==self.hashQ[i]):
                    break
            
            print("\n")


    # will be called in case-2 when any(first) free b1 will be removed for the required block number
    def setBlockNumber(self,oldBlockNumber,newBlockNumber):
        b1=self.findBlockInHashQ(oldBlockNumber)
        if(b1==None):
            b1=self.findInfl(oldBlockNumber)
        b1.setBlockNumber(newBlockNumber)


    # sets the lock bit for the b1 with supposed block number when removed from freelist
    def setLockedBit(self,blockNumber):
        b1=self.findBlockInHashQ(blockNumber)
        if(b1==None):
            b1=self.findInfl(blockNumber)
        b1.setLockedBit()
        
 	#clears the lock bit for the b1 with supposed block number when removed from hash queue
    def clearLockedBit(self,blockNumber):
        b1=self.findBlockInHashQ(blockNumber)
        if(b1==None):
            b1=self.findInfl(blockNumber)
        b1.clearLockedBit()
        
 	# checks if the lock bet is set or not
    def isLocked(self,blockNumber):
        b1=self.findBlockInHashQ(blockNumber)
        if(b1==None):
            b1=self.findInfl(blockNumber)
        return b1.isLocked()

    # sets this bit to indicate that b1 data is valid
    def setValidBit(self,blockNumber):
        block=self.findBlockInHashQ(blockNumber)
        if(block==None):
            block=self.findInfl(blockNumber)
        block.setValidBit()
        
    # clears this bit to indicate that b1 data is invalid
    def clearValidBit(self,blockNumber):
        block=self.findBlockInHashQ(blockNumber)
        if(block==None):
            block=self.findInfl(blockNumber)
        block.clearValidBit()
        
 	# checks if the b1 data is valid or not
    def isValid(self,blockNumber):
        block=self.findBlockInHashQ(blockNumber)
        if(block==None):
            block=self.findInfl(blockNumber)
        return block.isValid()
        
	# The b1 contents have not yet been written to the disk and it is marked as delayed
    def setDelayedWriteBit(self,blockNumber):
        b1=self.findBlockInHashQ(blockNumber)
        if(b1==None):
            b1=self.findInfl(blockNumber)
        b1.setDelayedWriteBit()
        
     # When the contents of the b1 has been written to the disk
    def clearDelayedWriteBit(self,blockNumber):
        b1=self.findBlockInHashQ(blockNumber)
        if(b1==None):
            b1=self.findInfl(blockNumber)
        b1.clearDelayedWriteBit()
	# Checks whether b1 is marked delayed or not
    def isDelayedWrite(self,blockNumber):
        b1=self.findBlockInHashQ(blockNumber)
        if(b1==None):
            b1=self.findInfl(blockNumber)
        return b1.isDelayedWrite()

