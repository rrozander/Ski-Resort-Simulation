from __future__ import annotations
from lift import Lift
from run import Run
from skier import Skier
from event import Event
import heapq
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(55627)

CLOSE_TIME = 6.5 * 60.0 # 9am to 3:30 pm = 6.5 hours = 390 minutes

def main():
  # Initialize the system
  event_queue: list[Event] = []
  sim_time = 0.0

  entry_lifts, all_lifts = initialize_runs_and_lifts()

  # Initialize with first resort arrival
  arrival_dt = Event.generateInterArrival(get_nspp_rate(sim_time))
  schedule(event_queue, Event((sim_time + arrival_dt), Event.EventType.RESORT_ARRIVAL, None, None))

  print("Starting simulation")

  # Loop until we hit a specified time on the simulation clock (Resort Closing Time)
  while event_queue:
    ev: Event = heapq.heappop(event_queue)
    current_time = ev.time

    if ev.etype == Event.EventType.RESORT_ARRIVAL:
      # create skier and send to random entry lift
      new_skier = Skier(arrival_time=current_time)
      # print(f"Skier {new_skier.id} arrives at resort {current_time:.2f} minutes")

      # schedule next resort arrival
      inter = Event.generateInterArrival(get_nspp_rate(current_time))
      schedule(event_queue, Event(current_time + inter, Event.EventType.RESORT_ARRIVAL, None, None))

      # Send to entry lift
      entry_lift: Lift = np.random.choice(entry_lifts, p=[0.35, 0.35, 0.1, 0.2])
      entry_lift.handle_arrival(current_time, new_skier, lambda e: schedule(event_queue, e))

    elif ev.etype == Event.EventType.LIFT_START:
      # call start_service method of lift
      lift: Lift = ev.obj
      lift.start_service(current_time, lambda e: schedule(event_queue, e))

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
  
  # Process any skiers still in the system at simulation end
  final_time = current_time if event_queue else CLOSE_TIME
  for skier in Skier.all_skiers:
    if skier.departure_time is None:
      skier.leave_resort(final_time)
  
  print_stats(all_lifts)

  print("Simulation complete")


def schedule(event_queue: list[Event], new_event: Event) -> None:
  """Schedules a new event by adding it to the event queue."""
  # Only prevent new arrivals after closing time - let all other events complete
  if new_event.etype == Event.EventType.RESORT_ARRIVAL and new_event.time > CLOSE_TIME:
    return
  heapq.heappush(event_queue, new_event)


def get_nspp_rate(current_time: float) -> float:
  """Non-stationary Poisson Process rate function for resort arrivals."""

  # Best guess at arrival rates, we can adjust as needed

  if current_time < 60.0:
    return 0.1  # High arrival rate in first hour
  elif current_time < 120.0:
    return 0.15
  elif current_time < 240.0:
    return 0.5
  elif current_time < 300.0:
    return 3.0
  elif current_time < CLOSE_TIME- 30.0:
    return 8.0  # Low arrival rate before closing
  else:
    return 0.0 # No arrivals in last 30 minutes


def print_stats(lifts: list[Lift]):
  # Use all_skiers instead of just skiers_processed to include everyone
  skiers: list[Skier] = sorted(Skier.all_skiers, key=lambda skier: skier.get_stats()['total_time_at_resort'], reverse=True)


  avg_total_time = np.mean([skier.get_total_time_at_resort() for skier in skiers])
  avg_wait_time = np.mean([skier.get_stats()['time_waiting_in_line'] for skier in skiers])
  avg_lift_time = np.mean([skier.get_stats()['time_on_lift'] for skier in skiers])
  avg_ski_time = np.mean([skier.get_stats()['time_skiing'] for skier in skiers])
  avg_runs = np.mean([skier.get_stats()['number_of_runs'] for skier in skiers])

  # for skier in skiers:
  #   stats = skier.get_stats()
  #   print(f"Skier {stats['id']}: " + 
  #         f"Total time: {stats['total_time_at_resort']:.2f} min, " + 
  #         f"Wait time: {stats['time_waiting_in_line']:.2f} min, " + 
  #         f"Lift time: {stats['time_on_lift']:.2f} min, " + 
  #         f"Skiing time: {stats['time_skiing']:.2f} min, " +
  #         f"Number of runs: {stats['number_of_runs']}")

  print(f"Total skiers processed: {len(skiers)}")
  print(f"Average total time at resort: {avg_total_time:.2f} minutes")
  print(f"Average wait time in line: {avg_wait_time:.2f} minutes")
  print(f"Average time on lifts: {avg_lift_time:.2f} minutes")
  print(f"Average time skiing: {avg_ski_time:.2f} minutes")
  print(f"Average number of runs completed: {avg_runs:.2f}")

  print("\nAverage Wait Time per Lift:")
  for lift in lifts:
      if lift.wait_times:
          avg_wait = np.mean(lift.wait_times)
          print(f"  {lift.name}: {avg_wait:.2f} minutes")
      else:
          print(f"  {lift.name}: 0.00 minutes (No skiers served)")

  # Create histogram of runs per skier
  runs = [skier.get_stats()['number_of_runs'] for skier in skiers]
  
  plt.figure(figsize=(10, 6))
  plt.hist(runs, bins=range(min(runs), max(runs) + 2), align='left', rwidth=0.8, edgecolor='black')
  plt.title('Distribution of Runs per Skier')
  plt.xlabel('Number of Runs')
  plt.ylabel('Number of Skiers')
  plt.grid(axis='y', alpha=0.75)
  plt.savefig('histograms/skier_runs_histogram.png')



def initialize_runs_and_lifts():
  # create all runs
  run_E_W = Run(name="E_W", avg_time=2, chance_to_take=0.1)
  run_E_H = Run(name="E_H", avg_time=6.5, chance_to_take=0.15)
  run_E_BB = Run(name="E_BB", avg_time=12.5, chance_to_take=0.1)
  run_E_S = Run(name="E_S", avg_time=10.5, chance_to_take=0.2) # Updated from 15%
  run_E_E = Run(name="E_E", avg_time=10.5, chance_to_take=0.4)
  run_E_Out = Run(name="E_Out", avg_time=0, chance_to_take=0.05) # Updated from 10%

  run_W_E = Run(name="W_E", avg_time=2, chance_to_take=0.25)
  run_W_S = Run(name="W_S", avg_time=8, chance_to_take=0.2) # Updated from 15%
  run_W_H = Run(name="W_H", avg_time=8, chance_to_take=0.15)
  run_W_W = Run(name="W_W", avg_time=10, chance_to_take=0.35)
  run_W_Out = Run(name="W_Out", avg_time=0, chance_to_take=0.05) # Updated from 10%

  run_S_S = Run(name="S_S", avg_time=10, chance_to_take=0.4)
  run_S_W = Run(name="S_W", avg_time=8, chance_to_take=0.15) # Updated from 10%
  run_S_E = Run(name="S_E", avg_time=8.5, chance_to_take=0.25)
  run_S_H = Run(name="S_H", avg_time=12, chance_to_take=0.15)
  run_S_Out = Run(name="S_Out", avg_time=0, chance_to_take=0.05) # Updated from 10%

  run_H_H = Run(name="H_H", avg_time=9, chance_to_take=0.5)
  run_H_E = Run(name="H_E", avg_time=7, chance_to_take=0.25) # Updated from 20%
  run_H_W = Run(name="H_W", avg_time=7.5, chance_to_take=0.05)
  run_H_BF = Run(name="H_BF", avg_time=6.5, chance_to_take=0.15)
  run_H_Out = Run(name="H_Out", avg_time=0, chance_to_take=0.05) # Updated from 10%

  run_BF_BF = Run(name="BF_BF", avg_time=7, chance_to_take=0.1)
  run_BF_H = Run(name="BF_H", avg_time=12, chance_to_take=0.15)
  run_BF_BB = Run(name="BF_BB", avg_time=12, chance_to_take=0.75)

  run_BB_BB = Run(name="BB_BB", avg_time=12, chance_to_take=0.55)
  run_BB_BF = Run(name="BB_BF", avg_time=7, chance_to_take=0.1) 
  run_BB_E = Run(name="BB_E", avg_time=9.5, chance_to_take=0.2)
  run_BB_H = Run(name="BB_H", avg_time=9.5, chance_to_take=0.15)

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
  run_H_BF.dest_lift = lift_BF

  # Runs that go *to* BB
  run_E_BB.dest_lift  = lift_BB
  run_BF_BB.dest_lift = lift_BB
  run_BB_BB.dest_lift = lift_BB   # BB → BB loop


  return [lift_H, lift_E, lift_W, lift_S], [lift_E, lift_W, lift_S, lift_H, lift_BF, lift_BB]  # entry lifts, all lifts


if __name__ == "__main__":
  main()