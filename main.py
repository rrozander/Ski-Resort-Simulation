from __future__ import annotations
from lift import Lift
from run import Run
from skier import Skier
from event import Event
import heapq
import numpy as np

np.random.seed(3)

CLOSE_TIME = 1 * 30.0
LAMBDA = 1 / 0.5   # mean 0.5 min between resort arrivals

def main():
  # Initialize the system
  event_queue: list[Event] = []
  sim_time = 0.0

  entry_lifts: list[Lift] = initialize_runs_and_lifts()

  # Initialize with first resort arrival
  arrival_dt = Event.generateInterArrival(LAMBDA)
  schedule(event_queue, Event((sim_time + arrival_dt), Event.EventType.RESORT_ARRIVAL, None, None))

  print("Starting simulation")

  # Loop until we hit a specified time on the simulation clock (Resort Closing Time)
  while event_queue:
    ev: Event = heapq.heappop(event_queue)
    current_time = ev.time
    if current_time > CLOSE_TIME:
      break

    if ev.etype == Event.EventType.RESORT_ARRIVAL:
      # create skier and send to random entry lift
      new_skier = Skier()
      print(f"Skier {new_skier.id} arrives at resort {current_time:.2f} minutes")
      
      # schedule next resort arrival
      inter = Event.generateInterArrival(LAMBDA)
      schedule(event_queue, Event(current_time + inter, Event.EventType.RESORT_ARRIVAL, None, None))

      # Send to entry lift
      # TODO we should pick this based on weights. Random for now
      entry_lift: Lift = np.random.choice(entry_lifts)
      entry_lift.handle_arrival(current_time, new_skier, lambda e: schedule(event_queue, e))

    elif ev.etype == Event.EventType.LIFT_DEPART:
      # call depart method of lift
      lift: Lift = ev.obj 

      lift.handle_departure(current_time, lambda e: schedule(event_queue, e))

    elif ev.etype == Event.EventType.RUN_FINISH:
      # call depart function of run
      # print(f"Run finish at time {current_time:.2f} minutes")
      run: Run = ev.obj

      run.handle_run_finish(current_time, ev.skier, lambda e: schedule(event_queue, e))
    
    # Time average statistics

    # Invoke next event function
  # Output results
  print("Simulation complete")
  pass



def schedule(event_queue: list[Event], new_event: Event) -> None:
  if new_event.time <= CLOSE_TIME:
    heapq.heappush(event_queue, new_event)

def initialize_runs_and_lifts():
  # create all runs
  run_E_W = Run(name="E_W", avg_time=0.5, chance_to_take=0.1)
  run_E_H = Run(name="E_H", avg_time=3.5, chance_to_take=0.15)
  run_E_BB = Run(name="E_BB", avg_time=12.5, chance_to_take=0.1)
  run_E_S = Run(name="E_S", avg_time=7.5, chance_to_take=0.15)
  run_E_E = Run(name="E_E", avg_time=7.5, chance_to_take=0.4)
  run_E_Out = Run(name="E_Out", avg_time=0, chance_to_take=0.1)

  run_W_E = Run(name="W_E", avg_time=0.5, chance_to_take=0.25)
  run_W_S = Run(name="W_S", avg_time=6, chance_to_take=0.15)
  run_W_H = Run(name="W_H", avg_time=4, chance_to_take=0.15)
  run_W_W = Run(name="W_W", avg_time=5, chance_to_take=0.35)
  run_W_Out = Run(name="W_Out", avg_time=0, chance_to_take=0.1)

  run_S_S = Run(name="S_S", avg_time=8, chance_to_take=0.4)
  run_S_W = Run(name="S_W", avg_time=6, chance_to_take=0.1)
  run_S_E = Run(name="S_E", avg_time=6.5, chance_to_take=0.25)
  run_S_H = Run(name="S_H", avg_time=10, chance_to_take=0.15)
  run_S_Out = Run(name="S_Out", avg_time=0, chance_to_take=0.1)

  run_H_H = Run(name="H_H", avg_time=7, chance_to_take=0.5)
  run_H_E = Run(name="H_E", avg_time=5, chance_to_take=0.2)
  run_H_W = Run(name="H_W", avg_time=5.5, chance_to_take=0.05)
  run_H_BF = Run(name="H_BF", avg_time=2.5, chance_to_take=0.15)
  run_H_Out = Run(name="H_Out", avg_time=0, chance_to_take=0.1)

  run_BF_BF = Run(name="BF_BF", avg_time=5, chance_to_take=0.1)
  run_BF_H = Run(name="BF_H", avg_time=10, chance_to_take=0.15)
  run_BF_BB = Run(name="BF_BB", avg_time=10, chance_to_take=0.75)

  run_BB_BB = Run(name="BB_BB", avg_time=10, chance_to_take=0.55)
  run_BB_BF = Run(name="BB_BF", avg_time=5, chance_to_take=0.1) 
  run_BB_E = Run(name="BB_E", avg_time=7.5, chance_to_take=0.2)
  run_BB_H = Run(name="BB_H", avg_time=7.5, chance_to_take=0.15)

  # create all lifts
  lift_E = Lift(
    "Lift E",
    [run_E_E, run_W_E, run_S_E, run_H_E, run_BB_E],
    [run_E_W, run_E_H, run_E_BB, run_E_S, run_E_E, run_E_Out],
    4,
    10
  )
  lift_W = Lift(
    "Lift W",
    [run_E_W, run_W_W, run_H_W, run_S_W],
    [run_W_E, run_W_S, run_W_H, run_W_W, run_W_Out],
    3, 
    10
  )
  lift_S = Lift(
    "Lift S",
    [run_E_S, run_W_S, run_S_S],
    [run_S_S, run_S_W, run_S_E, run_S_H, run_S_Out],
    4,
    15
  )
  lift_H = Lift(
    "Lift H",
    [run_E_H, run_W_H, run_S_H, run_BF_H, run_BB_H, run_H_H],
    [run_H_H, run_H_E, run_H_W, run_H_BF, run_H_Out],
    6,
    10
  )
  lift_BF = Lift(
    "Lift BF",
    [run_BF_BF, run_BB_BF, run_H_BF],
    [run_BF_BF, run_BF_H, run_BF_BB],
    4,
    5
  )
  lift_BB = Lift(
    "Lift BB",
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


  return [lift_H, lift_E, lift_W, lift_S]  # entry lifts


if __name__ == "__main__":
  main()