from main import Event  # or put Event in a shared module
from __future__ import annotations
from typing import List


class lift:
    def __init__(self, incoming_runs, outgoing_runs, capacity, speed):
        self.lift_capacity = capacity
        self.lift_speed = speed # How long it takes to ride the lift - in minutes
        self.lift_wait_time = 0 # Wait for a lift to arrive + pick people up - in minutes
        self.incoming_runs = incoming_runs # these should be objects containing percentages
        self.outgoing_runs = outgoing_runs

        self.queue = []
        self.in_service = None

    
    def get_outgoing_runs(self):
        pass
    
    def get_incoming_runs(self):
        pass

    # need a function to choose next run
    def chose_run():
        # first get array of weights
        weights = []

    def handle_arrival(self, t, skier, schedule):
        self.queue.append(skier)
        if self.in_service is None:
            self._start_service(t, schedule)

    def _start_service(self, t, schedule):
        if not self.queue:
            return
        self.in_service = self.queue.pop(0)
        depart_time = t + self.lift_speed
        schedule(Event(depart_time, "LIFT_DEPART", self, None))

    def handle_departure(self, t, schedule):
        skier = self.in_service
        self.in_service = None

        # run = self._choose_run()
        # run.handle_run_start(t, skier, schedule)

        if self.queue:
            self._start_service(t, schedule)
    