class lift:
    def __init__(self, incoming_runs, outgoing_runs, capacity, speed):
        self.lift_capacity = capacity
        self.lift_speed = speed # How long it takes to ride the lift - in minutes
        self.lift_wait_time = 0 # Wait for a lift to arrive + pick people up - in minutes
        self.incoming_runs = incoming_runs # these should be objects containing percentages
        self.outgoing_runs = outgoing_runs

        self.upcoming_events = [0, float('inf'), float('inf')] # next events array [0] not use, [1] for arrival, [2] for departure - may need to be changed
        self.lift_queue = [] # array of skier objects
        self.on_lift = [] # array of arrays of skier objects representning chairs on lift

    
    def get_outgoing_runs(self):
        pass
    
    def get_incoming_runs(self):
        pass

    def arrival_event(self):
        # Schedule next arrival event

        # Check the queue size to determain what to do
          # Less than capacity -> queue until we hit capacity
          # At capacity -> depart immediately
          # Over capacity -> Add to queue

        # Schedule departure 
        # maybe this should emit the time on lift so that it can be used to schedule arrival to next run
        # since incoming runs is an array of objects with the run class we could also just call the arrive event with the sim time
        pass
    
    def departure_event(self):
        
        pass
    