#  Defines two signal catcher functions.
# These functions are called by the target environment when the corresponding signal occurs.
# The target environment suspends execution of the program until the signal catcher returns.

import signal
import os

# This function generates signal for processes waiting for a particular buffer
def sigint_catcher(sig,frame):
    print("process: ",os.getpid()," woke up as it was sleeping for a particular buffer" )

#It generates the signal for processes waiting for any buffer
def sighup_catcher(sig,frame):
    print("process: ",os.getpid()," woke up as it was sleeping for a any buffer" )



    


