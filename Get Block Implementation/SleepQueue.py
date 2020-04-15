import time
import os

class SleepQueue(object):
    def __init__(self):
        self.sleepQueue={}

    def add(self,buffer,pid): #buffer-key         pid-value
        self.sleepQueue.setdefault(buffer,[])
        self.sleepQueue[buffer].append(pid)

    



    #-2 is returned if buffer not present
    #otherwise list of waiting processes are returned
    def getPidsWaitingForBuffer(self,buffer): 
        return self.sleepQueue.pop(buffer,-2)

    #as processes waiting for any buffer store -1 in buffer number
    def getPidsWaitingForAnyBuffer(self):
        return self.sleepQueue.pop(-1,-2)
