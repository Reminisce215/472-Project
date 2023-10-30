# 472 Project Report

# Functionalites

- Child Process Creation: At program's launch, a parent process is created in the main function to run the program script. Through the program's
command line interface, you are able to create a child process to the parent(main) process. With this program's implementation, all child processes
will stem from the original parent process. Its worth noting that in this code create process and fork have the same functionality as fork doesn't 
seem to be possible in a Windows environment. When a new process is created, it not child process that is not a copy of parent nor shares its memory
space. 

Child Process Creation
![process creation]()


- Process Listing/Terminate: We have the functionality to list processes and their respective threads. The event logging also keeps track of when a process has terminated.
As you can see, by the time I list the process it has terminated

![listing/terminate]()

- Exec System Call: We can also use the exec system call to perform various processes such as displaying all running proccesses, running calculator, show current directory,etc.

![exec]()

- Here is an example of functionality to create multiple threads within a process. When the a thread is created, create command and thread function are called. Within the thread function,
the shared variable is incremeneted by one for each created process. This shared variable allows for threads to share data among themselves. This data sharing using the multiprocession.value 
is an examploe of interprocess communication. 

![thread creation]()

- In my program I used the multiprocessing.Lock to syncrhonize acccess to resource queue. Lock ensures that only one thread can access shared data at a given time. This is done to prevent the
producing from overflowing the queue and to stop consumer from trying to consume data when queue is empty. Multiprocessing.queue is used as a shared buffer between producer and consumer.
To showcase syncrhonization, the producer and consumer are run in separate threads within a process. Producer generates data then sleeps for 1seconds, consumer removes data then sleeps for 1.5
seconds. 

![process synchronization]()



# Conclusion
This assignment required quite a few workrarounds due to Window's limited cross over with Unix OS functionality. For example, many of Python's os moduel operations such as os.fork and os.set/getuid. 
Forutnately, many of the issues had alternative operations with the multiprocessing module although I was not able to find a one to one solution for forking. All an all I learned alot system calls
and process and thread data sharing. 