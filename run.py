class run:
    def __init__(self, avg_time, chance_to_take):
        self.avg_run_time = avg_time # average time to complete the run - in minutes
        self.percentage_traffic = chance_to_take
        pass
    
    def arrival_event(self):
        # this should emit run time so that it can be used to schedule next lift arrival
        # will need to consider how to handle out runs (runs that leave resort)
        pass
    
    def departure_event(self):
        pass
