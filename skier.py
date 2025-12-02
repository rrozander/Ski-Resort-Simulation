class Skier:
  # this is a class to keep track of a skiers stats
  curr_id = 0

  def __init__(self):
    self.id = Skier.curr_id
    Skier.curr_id += 1
    self.time_in_line = 0
    self.time_on_lift = 0