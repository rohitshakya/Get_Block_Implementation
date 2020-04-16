#This class defines the SleepQueue,which maintains the record of sleeping processes.
#We have implemented this as dictionary where buffer is the key and pid is the value.

import time
import os

class SleepQueue(object):
    def __init__(self):
        self.sleepQueue={}

    def add(self,buffer,pid):
        self.sleepQueue.setdefault(buffer,[])
        self.sleepQueue[buffer].append(pid)

    #-2 is returned if buffer not present otherwise list of waiting processes are returned

    def getPidsWaitingForBuffer(self,buffer): 
        return self.sleepQueue.pop(buffer,-2)

    #processes waiting for any buffer store -1 in buffer number

    def getPidsWaitingForAnyBuffer(self):
        return self.sleepQueue.pop(-1,-2)
