class Skier:
  # this is a class to keep track of a skiers stats
  curr_id = 0
  skiers_processed = []

  def __init__(self, arrival_time: float = 0.0):
    self.id = Skier.curr_id
    Skier.curr_id += 1
    
    # Statistics
    self.arrival_time = arrival_time  # When the skier arrived at the resort
    self.departure_time = None  # When the skier left the resort
    self.time_in_line = 0.0  # Total time waiting in lift queues
    self.time_on_lift = 0.0  # Total time riding lifts
    
    # Temporary tracking variables
    self.current_queue_entry_time = None  # When skier entered current queue
    self.current_lift_start_time = None  # When skier started current lift ride
  
  def enter_queue(self, current_time: float) -> None:
    """Called when skier joins a lift queue."""
    self.current_queue_entry_time = current_time
  
  def start_lift(self, current_time: float) -> None:
    """Called when skier starts riding a lift."""
    if self.current_queue_entry_time is not None:
      # Add the wait time to total
      self.time_in_line += current_time - self.current_queue_entry_time
      self.current_queue_entry_time = None
    self.current_lift_start_time = current_time
  
  def finish_lift(self, current_time: float) -> None:
    """Called when skier finishes riding a lift."""
    if self.current_lift_start_time is not None:
      # Add the ride time to total
      self.time_on_lift += current_time - self.current_lift_start_time
      self.current_lift_start_time = None
  
  def leave_resort(self, current_time: float) -> None:
    """Called when skier exits the resort."""
    self.departure_time = current_time
    Skier.skiers_processed.append(self)
  
  def get_total_time_at_resort(self) -> float:
    """Returns total time spent at the resort."""
    if self.departure_time is not None:
      return self.departure_time - self.arrival_time
    return 0.0
  
  def get_stats(self) -> dict:
    """Returns a dictionary of all statistics."""
    return {
      'id': self.id,
      'total_time_at_resort': self.get_total_time_at_resort(),
      'time_waiting_in_line': self.time_in_line,
      'time_on_lift': self.time_on_lift,
      'time_skiing': self.get_total_time_at_resort() - (self.time_in_line + self.time_on_lift),
      'arrival_time': self.arrival_time,
      'departure_time': self.departure_time
    }

