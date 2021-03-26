Mobile Network system simulation
==============

The algorithm simulates a Mobile Network system in handling a current load that spans a highway connecting 2 major cities. It follows the same assumptions in the assignment that was simulated in Arena. The algorithm inputs the number of cell towers, channels per cell and number of reserved channels. It will then output the number of blocked and dropped calls over a 12 hour time period. 

The input takes in a boolean flag whether to conduct a replication or not.
The replication will be 20 runs of a 12 hours simulation with a 1hr warmup period, for 0 - 6 reserved channels. 

If replication is not selected, it takes in:
1) The number of cell towers 
2) The number of channels per cell tower
3) The number of channels to reserve under the FCA scheme 



# Requirements
- numpy
- random


# Implementation detail
Below are some examples showing how to run the <code>main.py
  
<code>$ python main.py </code> 

<code>Do you want to do replication? Y/N: N </code> 

<code>How many cell towers are there?: 20 </code> 

<code>How many channels are there per cell?: 10 </code> 

<code>How many channels do you want to reserve?: 4 </code> 
