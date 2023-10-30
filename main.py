import multiprocessing
import subprocess
import os
import psutil
import time
import threading
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)

def list_processes(created_processes):
    """List all running processes."""
    for pid in created_processes:
        try:
            p = psutil.Process(pid)
            logging.info("Process with PID {} is running.".format(pid))
        except psutil.NoSuchProcess:
            logging.warning("Process with PID {} has terminated.".format(pid))

def terminate_process(created_processes):
    """Terminate a specified process."""
    pid = int(input("Enter the PID of the process to terminate: "))
    if pid in created_processes:
        try:
            p = psutil.Process(pid)
            p.terminate()
            logging.info("Process with PID {} terminated successfully.".format(pid))
            created_processes.remove(pid)  # remove the PID from the list
        except psutil.NoSuchProcess:
            logging.error("Error: process with PID {} not found.".format(pid))
    else:
        logging.error("Error: process with PID {} is not within the scope of this project.".format(pid))

def thread_function(thread_id, shared_variable):
    """Function to be run by each thread."""
    logging.info("Thread {} in process with PID: {} started.".format(thread_id, os.getpid()))
    shared_variable.value += 1
    logging.info("Shared variable value is now: {}".format(shared_variable.value))
    time.sleep(5)  # Simulate thread work
    logging.info("Thread {} in process with PID: {} finished.".format(thread_id, os.getpid()))

def producer(queue, lock):
    """Function to produce items and add them to the queue."""
    for i in range(5):
        with lock:
            logging.info('Producing item %d', i)
            queue.put(i)
            time.sleep(1)

def consumer(queue, lock):
    """Function to consume items from the queue."""
    for i in range(5):
        with lock:
            if not queue.empty():
                item = queue.get()
                logging.info('Consuming item %d', item)
            time.sleep(1.5)

def child_process(queue, shared_variable, pipe_conn):
    """Function to be run by each child process."""
    logging.info("Child process with PID: {} started.".format(os.getpid()))
    threads = []
    while True:
        choice = queue.get()

        if choice == 'create':
            thread_id = len(threads)
            thread = threading.Thread(target=thread_function, args=(thread_id, shared_variable))
            thread.start()
            threads.append(thread)
            logging.info("Created thread {} in process with PID: {}.".format(thread_id, os.getpid()))

        elif choice == 'terminate':
            thread_id = int(queue.get())
            if 0 <= thread_id < len(threads):
                thread = threads[thread_id]
                thread.join()
                logging.info("Terminated thread {} in process with PID: {}.".format(thread_id, os.getpid()))

        elif choice == 'list':
            for i, thread in enumerate(threads):
                if thread.is_alive():
                    logging.info("Thread {} is running.".format(i))
                else:
                    logging.info("Thread {} has terminated.".format(i))

        elif choice == 'producer_consumer':
            lock = multiprocessing.Lock()
            q = multiprocessing.Queue()
            producer_thread = threading.Thread(target=producer, args=(q, lock))
            consumer_thread = threading.Thread(target=consumer, args=(q, lock))

            producer_thread.start()
            consumer_thread.start()

            producer_thread.join()
            consumer_thread.join()

        elif choice == 'exit':
            for thread in threads:
                thread.join()
            pipe_conn.send("Child process with PID: {} is exiting.".format(os.getpid()))
            pipe_conn.close()
            logging.info("Child process with PID: {} exited.".format(os.getpid()))
            break

        else:
            logging.warning("Invalid choice received: {}".format(choice))

def main():
    """Main function to handle user inputs and manage processes."""
    parent_pid = os.getpid()
    print("Parent process ID: {}".format(parent_pid))
    created_processes = []
    queue = multiprocessing.Queue()
    shared_variable = multiprocessing.Value("i", 0)
    parent_conn, child_conn = multiprocessing.Pipe()

    while True:
        choice = input(
            "Enter 'create' to create a new process, 'fork' to fork a process, 'exec' to replace the process, "
            "'list' to list running processes, 'terminate' to terminate a process, 'producer_consumer' to run the producer-consumer example or 'exit' to quit: ")

        if choice == 'create' or choice == 'fork':
            p = multiprocessing.Process(target=child_process, args=(queue, shared_variable, child_conn))
            p.start()
            created_processes.append(p.pid)
            logging.info("Created process with PID: {}".format(p.pid))

            while True:
                child_choice = input(
                    "Enter 'create' to create a new thread, 'terminate' to terminate a thread, 'list' to list running threads, 'producer_consumer' to run the producer-consumer example or 'exit' to exit the thread manager: ")
                queue.put(child_choice)
                if child_choice == 'exit':
                    break

                if child_choice == 'terminate':
                    thread_id = input("Enter the thread ID to terminate: ")
                    queue.put(thread_id)

            p.join()
            logging.info(parent_conn.recv())

        elif choice == 'exec':
            cmd = input("Enter a command to run: ")
            subprocess.run(cmd, shell=True)

        elif choice == 'list':
            list_processes(created_processes)  # Fixed

        elif choice == 'terminate':
            terminate_process(created_processes)  # Added

        elif choice == 'exit':
            break

if __name__ == "__main__":
    main()
