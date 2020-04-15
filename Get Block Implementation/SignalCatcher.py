import signal
import os


#signal for processes waiting for a particular buffer
def sigint_catcher(sig,frame):
    print("process: ",os.getpid()," woke up as it was sleeping for a particular buffer" )

#signal for processes waiting for any buffer
def sighup_catcher(sig,frame):
    print("process: ",os.getpid()," woke up as it was sleeping for a any buffer" )



    


