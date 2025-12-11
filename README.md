# Ski-Resort-Simulation
Ski lift simulation project for UVic CSC 446 (Simulations in Operations Research)

The casy study for this particular simulation will be Mount Washington Ski Resort located on Vancouver Island.

The associated report can be downloaded and viewed here: [CSC 446 Project Report.pdf](https://github.com/user-attachments/files/24093221/CSC.446.Project.Report.pdf)

## Purpose
- Design and implement a discrete-event simulation of the resort lift and runs.
- Evaluate key metrics that include the average wait time, lift utilization, and total skier throughput.
- Explore optimizations to the system, such as adjusting lift capacities/speeds and reconfiguring the queue network (newer runs/connections, new lifts, etc.) This will help to inform the resort on what the system bottlenecks are and give evidence on what should be upgraded.

## Description
 The simulated resort would be made of a small queueing network:
- **3-5 Lifts (Nodes)**: These would be the nodes that are made up of a queuing system (Most likely a batch queuing system with deterministic service time and customer pickup time). 
- **Connecting Runs (Edges)**: Skiers travel on these from one lift to another. Here there will be set probabilities for where the skier goes when leaving a lift (same lift, different lift, leave resort, etc.). There will also be a set "Travel Time" when moving through these edges.
- **Skiers (Customers)**: Arrive at the base area following a poisson distribution.
    
### Queueing Network
Here is the run and lift network for Mount Washington Ski Resort that is used as reference for creating the queueing network used in the simulation.

<img width="2170" height="1826" alt="MountWashingtonTrailMap_compressed-1" src="https://github.com/user-attachments/assets/3ebd5e7c-9252-485e-a747-06937f29cbb0" />


The resulting queueing network with the assumed probabilities for moving through the resort is shown below.
<img width="700" height="1000" alt="LiftNetwork" src="https://github.com/user-attachments/assets/25efd234-6d43-4a2b-9b87-678b89d8f67d" />

## Results 
A summary of the results can be viewed in the graph below.

<img width="1200" height="600" alt="results_graph" src="https://github.com/user-attachments/assets/8b0988a8-554a-40bf-9361-4bc273416bcb" />
