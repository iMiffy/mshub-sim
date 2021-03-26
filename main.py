import random
import numpy as np
from pqueue import *

def mainFunction(HO_reserve, stationNum = 20, channelLimit = 10):
    workspace = pqueue() # Global event coordinator
    # arrivTime, TYPE, cellNum, callDuration, carSpeed, startPos, NOTES, uniqID

##    stationNum = 20
##    channelLimit = 10
    normalLimit = channelLimit - HO_reserve
    if normalLimit < 0: return 0

    print('Loading data...')
    uniqID = 0
    arrivTime = 0
    while arrivTime < 12 * 60 * 60: # 12hours
        arrivTime += np.random.exponential(1.35)            # cumulative, in seconds @@@ 1.35
        cellNum = random.randint(0, stationNum-1)           # cell num 0 to 19
        callDuration = np.random.exponential(119)           # In seconds   
        carSpeed = np.random.triangular(70, 90.1, 110)/60/60# from km/hr to km/sec
        startPos = random.random() * 2                      # Uniform between 2km diameter
        workspace.add( (arrivTime, 0, cellNum, callDuration, carSpeed, startPos, None, uniqID) )
        uniqID += 1
    arrNum = len(workspace.arr)

    print('Parameters:')
    print(f'Number of arrivals: {arrNum}')
    print(f'Number of cells: {stationNum}')
    print(f'Channel numbers: {channelLimit}')
    print(f'Channels to reserve: {HO_reserve}')

    stationArr = [(0, 0)] * stationNum # Normal channel, Reserved Channels
    blocked = []
    dropped = []
    
    runCounter = set()
    while workspace.arr:
        data = workspace.pop()
        arrivTime, TYPE, cellNum, callDuration, carSpeed, startPos, NOTES, uniqID = data
        if arrivTime <= 1 * 60 * 60: # 1 hour warmup
            blocked = []
            dropped = []
            runCounter = set()
        elif arrivTime >= 12* 60 * 60: break # Cutoff 12hour mark

        runCounter.add(uniqID)
        normalChannel, reserveChannel = stationArr[cellNum]

        # TYPE = 0 (arrival), 1 (handover), 2 (leaving)
        if TYPE == 0 or TYPE == 1:
            if normalChannel + reserveChannel < channelLimit and \
               (TYPE == 1 or (TYPE == 0 and normalChannel < normalLimit)):
                    # There are available channels
                    normalFlag = True
                    if TYPE == 0: stationArr[cellNum] = (normalChannel+1, reserveChannel)
                    if TYPE == 1:
                        if reserveChannel < HO_reserve:
                            stationArr[cellNum] = (normalChannel, reserveChannel+1)
                            normalFlag = False
                        else: stationArr[cellNum] = (normalChannel+1, reserveChannel)
                    
                    timeToSpend = (2-startPos)/carSpeed # Time spent in this cell
                    if timeToSpend < callDuration:
                        # Leaving entry
                        workspace.add(( arrivTime + timeToSpend, 2, cellNum, \
                                        None, None, None, normalFlag, uniqID) )
                        
                        # Add the handover
                        # Notes: Callduration - timeToSpend in this cell, startPos is 0, cellNum % for boundary
                        workspace.add(( arrivTime + timeToSpend, 1, (cellNum+1) % stationNum, \
                                        callDuration - timeToSpend, carSpeed, 0, normalFlag, uniqID) )
                    else:
                        # leave cell by call duration
                        workspace.add(( arrivTime + callDuration, 2, cellNum, \
                                        None, None, None, normalFlag, uniqID) ) 
            else:
                # No available channels                    
                if TYPE == 0: blocked.append( data )
                if TYPE == 1: dropped.append( data )
                
        elif TYPE == 2: # Leaving
            # startPos is normalFlag
            if NOTES: stationArr[cellNum] = (normalChannel-1, reserveChannel)
            else: stationArr[cellNum] = (normalChannel, reserveChannel-1)
    
    print(f'Blocked {len(blocked)}, {len(blocked)/arrNum*100:2f}%')
    print(f'Dropped {len(dropped)}, {len(dropped)/arrNum*100:2f}%')
    print('Final Time (secs)', arrivTime)
    print('Final Time (hours)', arrivTime/60/60)
    return (HO_reserve, len(blocked), len(dropped), arrNum, len(runCounter))

answer = input('Do you want to do replication? Y/N: ')
if answer == 'Y':
    import time
    print('Replication: 12 hrs, 1hr warmup, reserve 0-7 x 20')
    ansArr = []
    tic = time.perf_counter()
    for reserveChannels in range(7):
        tempArr = []
        for replication in range(20):
            tempArr.append( mainFunction(reserveChannels) )
            print(f'Current Time taken: {time.perf_counter()}s')
            print()
        print(tempArr)
        ansArr.append(tempArr)
        print()
    print(ansArr)

elif answer == 'N':
    cellNum = int(input('How many cell towers are there?: '))
    channelNumber = int(input('How many channels are there per cell?: '))
    reserveChannels = int(input('How many channels do you want to reserve?: '))
    
    mainFunction(reserveChannels, cellNum, channelNumber)


