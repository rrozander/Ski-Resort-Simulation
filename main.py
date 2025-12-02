from lift_run import lift, run
from event import Event
import heapq
import numpy as np

np.random.seed(3)
class Skier:
  # this is a class to keep track of a skiers stats
  def __init__(self):
    self.time_in_line = 0
    self.time_on_lift = 0

def main():
  # Initialize the system
  CLOSE_TIME = 8 * 60.0
  LAMBDA = 1 / 0.5   # mean 0.5 min between resort arrivals
  event_queue = []   # heap of Event
  sim_time = 0.0

  # create all runs
  run_E_W = run(avg_time=0.5, chance_to_take=0.1)
  run_E_H = run(avg_time=3.5, chance_to_take=0.15)
  run_E_BB = run(avg_time=12.5, chance_to_take=0.1)
  run_E_S = run(avg_time=7.5, chance_to_take=0.15)
  run_E_E = run(avg_time=7.5, chance_to_take=0.4)
  run_E_Out = run(avg_time=0, chance_to_take=0.1)

  run_W_E = run(avg_time=0.5, chance_to_take=0.25)
  run_W_S = run(avg_time=6, chance_to_take=0.15)
  run_W_H = run(avg_time=4, chance_to_take=0.15)
  run_W_W = run(avg_time=5, chance_to_take=0.35)
  run_W_Out = run(avg_time=0, chance_to_take=0.1)

  run_S_S = run(avg_time=8, chance_to_take=0.4)
  run_S_W = run(avg_time=6, chance_to_take=0.1)
  run_S_E = run(avg_time=6.5, chance_to_take=0.25)
  run_S_H = run(avg_time=10, chance_to_take=0.15)
  run_S_Out = run(avg_time=0, chance_to_take=0.1)

  run_H_H = run(avg_time=7, chance_to_take=0.5)
  run_H_E = run(avg_time=5, chance_to_take=0.2)
  run_H_W = run(avg_time=5.5, chance_to_take=0.05)
  run_H_BF = run(avg_time=2.5, chance_to_take=0.15)
  run_H_Out = run(avg_time=0, chance_to_take=0.1)

  run_BF_BF = run(avg_time=5, chance_to_take=0.1)
  run_BF_H = run(avg_time=10, chance_to_take=0.15)
  run_BF_BB = run(avg_time=10, chance_to_take=0.75)

  run_BB_BB = run(avg_time=10, chance_to_take=0.55)
  run_BB_BF = run(avg_time=5, chance_to_take=0.1) 
  run_BB_E = run(avg_time=7.5, chance_to_take=0.2)
  run_BB_H = run(avg_time=7.5, chance_to_take=0.15)

  # create all lifts
  lift_E = lift(
    [run_E_E, run_W_E, run_S_E, run_H_E, run_BB_E],
    [run_E_W, run_E_H, run_E_BB, run_E_S, run_E_E, run_E_Out],
    4,
    10
  )
  lift_W = lift(
    [run_E_W, run_W_W, run_H_W, run_S_W],
    [run_W_E, run_W_S, run_W_H, run_W_W, run_W_Out],
    3, 
    10
  )
  lift_S = lift(
    [run_E_S, run_W_S, run_S_S],
    [run_S_S, run_S_W, run_S_E, run_S_H, run_S_Out],
    4,
    15
  )
  lift_H = lift(
    [run_E_H, run_W_H, run_S_H, run_BF_H, run_BB_H, run_H_H],
    [run_H_H, run_H_E, run_H_W, run_H_BF, run_H_Out],
    6,
    10
  )
  lift_BF = lift(
    [run_BF_BF, run_BB_BF, run_H_BF],
    [run_BF_BF, run_BF_H, run_BF_BB],
    4,
    5
  )
  lift_BB = lift(
    [run_BB_BB, run_BF_BB, run_E_BB],
    [run_BB_BB, run_BB_BF, run_BB_E, run_BB_H],
    4,
    15
  )

  # assign dest lift for each run - all out runs should have dest lift = None
  # Runs that go *to* E
  run_W_E.dest_lift  = lift_E
  run_S_E.dest_lift  = lift_E
  run_H_E.dest_lift  = lift_E
  run_BB_E.dest_lift = lift_E
  run_E_E.dest_lift  = lift_E   # E → E loop
  run_E_Out.dest_lift = None    # leaves resort

  # Runs that go *to* W
  run_E_W.dest_lift  = lift_W
  run_S_W.dest_lift  = lift_W
  run_H_W.dest_lift  = lift_W
  run_W_W.dest_lift  = lift_W   # W → W loop
  run_W_Out.dest_lift = None    # leaves resort

  # Runs that go *to* S
  run_E_S.dest_lift  = lift_S
  run_W_S.dest_lift  = lift_S
  run_S_S.dest_lift  = lift_S   # S → S loop
  run_S_Out.dest_lift = None

  # Runs that go *to* H
  run_E_H.dest_lift  = lift_H
  run_W_H.dest_lift  = lift_H
  run_S_H.dest_lift  = lift_H
  run_BF_H.dest_lift = lift_H
  run_BB_H.dest_lift = lift_H
  run_H_H.dest_lift  = lift_H   # H → H loop
  run_H_Out.dest_lift = None

  # Runs that go *to* BF
  run_BF_BF.dest_lift = lift_BF   # BF → BF loop
  run_BB_BF.dest_lift = lift_BF

  # Runs that go *to* BB
  run_E_BB.dest_lift  = lift_BB
  run_BF_BB.dest_lift = lift_BB
  run_BB_BB.dest_lift = lift_BB   # BB → BB loop

  # Scheduler function
  def schedule(event):
    if event.time <= CLOSE_TIME:
      heapq.heappush(event_queue, event)

  # initialize with first resort arrival
  arrival_dt = Event.generateInterArrival(LAMBDA)
  schedule(Event((sim_time + arrival_dt), "RESORT_ARRIVAL", None, None))

  # Loop until we hit a specified time on the simulation clock (Resort Closing Time)
  while event_queue:
    ev = heapq.heappop(event_queue)
    current_time = ev.time
    if current_time > CLOSE_TIME:
      break

    if ev.etype == "RESORT_ARRIVAL":
      # create skier and send to random entry lift
      skier = Skier()
        
      # schedule next resort arrival
      inter = Event.generateInterArrival(LAMBDA)
      schedule(Event(current_time + inter, "RESORT_ARRIVAL", None, None))

    elif ev.etype == "LIFT_DEPART":
      # call depart method of lift
      pass

    elif ev.etype == "RUN_FINISH":
      # call depart function of run
      pass
    
    # Time average statistics

    # Invoke next event function

  # Output results
  pass