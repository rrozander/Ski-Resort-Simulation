from enum import Enum
import numpy as np

class Event:
  class EventType(Enum):
    RESORT_ARRIVAL = 1
    LIFT_DEPART = 2
    RUN_FINISH = 3

  def __init__(self, time: float, etype: EventType, obj, skier=None):
    self.time = time
    self.etype = etype
    self.obj = obj          # Lift or Run or None
    self.skier = skier      # Skier

  def generateInterArrival(mean: float) -> float:
    """Function to generate exponential random variates."""
    return -mean * np.log(np.random.uniform(0, 1))
