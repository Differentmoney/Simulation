import random
import simpy
import argparse

RANDOM_SEED = 42
SIM_TIME = 10
TIME= 0
LATENCY = 2
FIXED = False
MAX_LATENCY = 3
LPs = 1
RT = 0

parser = argparse.ArgumentParser()
parser.add_argument('-p', action="store", dest="LPs", default=LPs, type=int)
parser.add_argument('-s', action="store", dest="SIM_TIME",
                    default=SIM_TIME, type=int)
parser.add_argument('-f', action="store_true", dest="FIXED", default=False)
parser.add_argument('-k', action="store", dest="MAX_LATENCY",
                    default=MAX_LATENCY, type=int)
args = parser.parse_args()
LPs = args.LPs
SIM_TIME = args.SIM_TIME
FIXED = args.FIXED
MAX_LATENCY = args.MAX_LATENCY

print("-p {:<10} (LPs)".format(LPs))
print("-s {:<10} (SIM_TIME)".format(SIM_TIME))
print("-f {:<10} (FIXED)".format(FIXED))
print("-k {:<10} (MAX_LATENCY)".format(MAX_LATENCY))

#Pinging event, recursive
def ping(env, destLP):
   # while True:
    wtime=0
    #Set latency to fixed time if flag set, else random
    if(FIXED):
        wtime = LATENCY
    else:
        wtime = random.randint(1, MAX_LATENCY)
    yield env.timeout(wtime)    #wait due to latency
    global RT
    RT= RT + 1    #increment num trip
    destLP= destLP % LPs   #determine next LPs in order
    env.process(ping(env, destLP))

env = simpy.Environment()
env.process(ping(env, 0))
env.run(until=SIM_TIME)
print("Total Trips: "+ str(RT))
print("Round Trips: "+ str(RT/LPs))
