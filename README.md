<center><h1> Get Block Algorithm </h1></center>

<br>

Academic project to implement Getblk. We are aiming to simulate buffer management in UNIX system.

## Language used : 

 Python

## Installation :
You need to install the following things for running the code -
- Python3
- Windows Subsystem for Linux(WSL) (on Windows system)

## To execute :
1. run [DriverProcess.py](DriverProcess.py) 

## Code structure :
The structure is as follows :
* [DriverProcess.py](DriverProcess.py)  : This is our driver class. It imports *multiprocessing* package provided by python that supports spawning processes. It creates an object of BaseManager class so that the processes can access the shared objects by using proxy classes.

* [BufferHeader.py](BufferHeader.py) : Defines the buffer header and functions to access and change(only status bits) the block number and status bits. 

* [BufferDataStructure.py](BufferDataStructure.py) : Defines the basic structure of the data structures used in buffer cache : freelist and hashqueues. Also provides several functions to manipulate them (add,remove,printe etc)

* [myProcess.py](myProcess.py) : Simulates the functions of the process. Consists of three fuctions :
    1. pseudoOperation() : To simulate various cases like write, I/O error etc randomly.
    2. pseudoBrealse() : Function to release the buffer 
    3. process() : Target function called, when a process is created. Generates request for any block(within the given range;0 - number of blocks) and calls pseudoOperation(). After using the buffer, it releases that.

* [BufferManagement.py](BufferManagement.py) : This is the class which implements getBlk algorithm (getblock()). getblk() function used for acquiring buffers from a buffer cache pool. This class also contains two more functions : mySleepForBuffer() and mySleepForAnyBuffer(). These are our own sleep functions to sleep the process  waiting for buffers.  

* [AsynchronousWrite.py](AsynchronousWrite.py) : Used only in case of 'Delayed write' case. This allows asynchronous write on the disk.

* [SignalCatcher.py](SignalCatcher.py) : Defines two signal catcher functions. These functions are called by the target environment when the corresponding signal occurs. The target environment suspends execution of the program until the signal catcher returns.

* [SleepQueue.py](SleepQueue.py) : This class defies the SleepQueue, which maintains the record of sleeping processes. We have implemented this as dictionary where buffer is the key and pid is the value. 


## Code Flow : 
* The driver class ([DriverProcess.py](DriverProcess.py)) creates shared memory(BufferDataStructure and SleepQueue) using BaseManager class of multiprocessing library. Managers provide a way to create data which can be shared between different processes. A manager object is returned by BaseManager() which allows other processes to manipulate them using proxies. It initialises 4 empty has queues and a freelist of 20 buffers.  

* Then creates three processes and starts them. Each process starts its activity and calls the target callable object (i.e. Process.process()). After every 2 seconds, the process requests for the desired block number and getblock is called to allocate a buffer to the requesting process. 

* The getblock function takes the block number and checks whether the buffer is in corresponding hash queue :
    1. If the buffer is in hash queue.
        * And marked busy, the process goes to sleep, there by scheduling another process to run(which may again request for the same block). 
        * Otherwise, the function returns the buffer to the requesting process and marks it busy. 
    2. If the buffer is not in hash queue. Then, it checks the freelist. 
        * If freelist is empty then the process goes to sleep waiting for any buffer to get free. 
        * Otherwise, picks the first block from freelist and checks whether it is marked as "delayed write", if yes, then calls asynchronousWrite() and removes the buffer from the freelist. Otherwise, removes the first buffer(head) from the freelist and current hashqueue, updates block number, adds to the new hash queue. Finally, sets the status bits of the buffer and returns it to the requesting process.

* Once the process recieves a buffer, any situation may take place(using pseudoOperation() to simulate this). And finally,the process releases the acquired buffer via pseudoBrelse(). This function then wakes up all the processes sleeping for any buffer and a particular buffer by the interrupt handler routine.
