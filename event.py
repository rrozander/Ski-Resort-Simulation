from enum import Enum
import numpy as np

class Event:
  class EventType(Enum):
    RESORT_ARRIVAL = 1
    LIFT_START = 2
    LIFT_DEPART = 3
    RUN_FINISH = 4

  def __init__(self, time: float, etype: EventType, obj, skier=None):
    self.time = time
    self.etype = etype
    self.obj = obj          # Lift or Run or None
    self.skier = skier      # Skier

  def __lt__(self, other):
    """Compare events by time for heap ordering."""
    return self.time < other.time

  def generateInterArrival(mean: float) -> float:
    """Function to generate exponential random variates."""
    if mean == 0.0:
      return float('inf')  # No arrivals
    
    return -mean * np.log(np.random.uniform(0, 1))
