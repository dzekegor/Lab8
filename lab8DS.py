from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime


def calc_recv_timestamp(recv_time_stamp, counter):
    for i  in range(len(counter)):
        counter[i] = max(recv_time_stamp[i], counter[i])
    return counter

def event(pid, counter):
    counter[pid] += 1
    return counter

def send(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Dzek is lutshiy dog', counter))
    return counter

def recv(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    return counter

def process_one(pipe12):
    pid = 0
    counter = [0,0,0]
    counter = send(pipe12, pid, counter)
    counter = send(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv(pipe12, pid, counter)
    print("Process a:",counter)

def process_two(pipe21, pipe23):
    pid = 1
    counter = [0,0,0]
    counter = recv(pipe21, pid, counter)
    counter = recv(pipe21, pid, counter)
    counter = send(pipe21, pid, counter)
    counter = recv(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send(pipe21, pid, counter)
    counter = send(pipe23, pid, counter)
    counter = send(pipe23, pid, counter)
    print("Process b:",counter)

def process_three(pipe32):
    pid = 2
    counter = [0,0,0]
    counter = send(pipe32, pid, counter)
    counter = recv(pipe32, pid, counter)
    counter = event(pid, counter)
    counter = recv(pipe32, pid, counter)
    print("Process c:",counter)

if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one, 
                       args=(oneandtwo,))
    process2 = Process(target=process_two, 
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_three, 
                       args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
