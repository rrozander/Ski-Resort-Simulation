from lift import lift
from run import run
class Skier:
  # this is a class to keep track of a skiers stats
  def __init__(self):
    self.time_in_line = 0
    self.time_on_lift = 0

  

def main():
# Initialize the system
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

  # Loop until we hit a specified time on the simulation clock (Resort Closing Time)
  while True:
    # Find next event type
    pass
    # Time average statistics

    # Invoke next event function


    

  # Output results
  pass