"""
Ping pong program
- Scenario:
    Returns number of roundtrips from ping to pong given sim_time
"""
import random
import simpy
import argparse

RANDOM_SEED = 42
SIM_TIME = 10
TIME= 0
LATENCY = 2
FIXED = False
MAX_LATENCY = 3

parser = argparse.ArgumentParser()
parser.add_argument('-s', action="store", dest="SIM_TIME",
                    default=SIM_TIME, type=int)
parser.add_argument('-f', action="store_true", dest="FIXED", default=False)
parser.add_argument('-k', action="store", dest="MAX_LATENCY",
                    default=MAX_LATENCY, type=int)
args = parser.parse_args()
SIM_TIME = args.SIM_TIME
FIXED = args.FIXED
MAX_LATENCY = args.MAX_LATENCY

print("-s {:<10} (SIM_TIME)".format(SIM_TIME))
print("-f {:<10} (FIXED)".format(FIXED))
print("-k {:<10} (MAX_LATENCY)".format(MAX_LATENCY))

RT = 0
def ping(env):
   # while True:
    wtime=0
    #Set latency time to fixed if flag set, else random
    if(FIXED):
        wtime = LATENCY
    else:
        wtime = random.randint(1, MAX_LATENCY)
    yield env.timeout(wtime)  #wait for bounce to travel due to latency
    env.process(pong(env))
       
def pong(env):
    yield env.timeout(0)
    global RT
    RT = RT + 1     #registers the bounce and increment the trip
    #print("pong")
    env.process(ping(env))
env = simpy.Environment()
env.process(ping(env))
env.run(until=SIM_TIME)
print(RT)
