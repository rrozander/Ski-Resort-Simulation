class lift:
    def __init__(self, incoming_runs, outgoing_runs):
        lift_capacity = 0
        lift_speed = 0 # How long it takes to ride the lift
        lift_wait_time = 0 # Wait for a lift to arrive + pick people up

        pass
    
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

        pass
    
    def departure_event(self):
        
        pass
    