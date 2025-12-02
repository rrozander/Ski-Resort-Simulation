import numpy as np

class Event:
  def __init__(self, time, etype, obj, skier=None):
    self.time = time
    self.etype = etype      # "RESORT_ARRIVAL", "LIFT_DEPART", "RUN_FINISH"
    self.obj = obj          # Lift or Run or None
    self.skier = skier      # Skier

  def generateInterArrival(mean):
    """Function to generate exponential random variates."""
    return -mean * np.log(np.random.uniform(0, 1))