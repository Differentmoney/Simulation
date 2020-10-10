import random
import simpy
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from queue import PriorityQueue

RANDOM_SEED = 42
SIM_TIME = 10
TIME= 0
LATENCY = 2
FIXED = False
MAX_LATENCY = 3
LPs = 1
RT = 0
MSG = 30
COL = '1'

parser = argparse.ArgumentParser()
parser.add_argument('-p', action="store", dest="LPs", default=LPs, type=int)
parser.add_argument('-s', action="store", dest="SIM_TIME",
                    default=SIM_TIME, type=int)
parser.add_argument('-f', action="store_true", dest="FIXED", default=False)
parser.add_argument('-k', action="store", dest="MAX_LATENCY",
                    default=MAX_LATENCY, type=int)
parser.add_argument('-m', action="store", dest="MSG", default=MSG, type=int)

args = parser.parse_args()
LPs = args.LPs
SIM_TIME = args.SIM_TIME
FIXED = args.FIXED
MAX_LATENCY = args.MAX_LATENCY
MSG = args.MSG

print("-p {:<10} (LPs)".format(LPs))
print("-s {:<10} (SIM_TIME)".format(SIM_TIME))
print("-f {:<10} (FIXED Latency)".format(FIXED))
print("-k {:<10} (MAX_LATENCY)".format(MAX_LATENCY))
print("-m {:<10} (Messages)".format(MSG))
   
#Set up Priority Queue for messages!
message = PriorityQueue()
for x in range(MSG):
    message.put(x)

#Define ping event to a LP or bounce, this event is recursive
def ping(env, next_item, fromLP):
    wtime=0
    #Sets latency based on flag else random
    if(FIXED):
        wtime = LATENCY
    else:
        wtime = random.randint(1, MAX_LATENCY)
    yield env.timeout(wtime)    # wait due to latency
    global RT
    #Determines if message is sent to itself or another LP
    while True:
        destLP = random.randint(0, LPs)
        if(destLP != fromLP):
            RT = RT + 1
            break
    env.process(ping(env, next_item, destLP))


env = simpy.Environment()
count=0     #denotes number of messages sent
fromLP=0    #denotes from which LP msg came from
#Central while loop to run sim until time specified
while not message.empty():
    count = count + 1
    next_item= message.get()    # pops next message from Priority Queue
    if((count % LPs) == 0):     # evenly distributes messages to each LP
        fromLP=LPs
    else:
        fromLP= next_item % LPs
    env.process(ping(env, next_item, fromLP))
    
env.run(until=SIM_TIME)
print(RT)


