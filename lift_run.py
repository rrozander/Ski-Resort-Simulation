from main import generateInterArrival
from main import Event
from __future__ import annotations
from typing import List
import numpy as np

np.random.seed(3)

class run:
    def __init__(self, avg_time: float, chance_to_take: float):
        self.avg_run_time = avg_time # average time to complete the run - in minutes
        self.chance_to_take = chance_to_take
        self.next_lift = None  # type: lift | None

    def handle_run_start(self, t, skier, schedule):
        if self.avg_run_time <= 0:
            self.handle_run_finish(t, skier, schedule)
            return
        run_time = generateInterArrival(self.avg_run_time)
        finish_time = t + run_time
        schedule(Event(finish_time, "RUN_FINISH", self, skier))

    def handle_run_finish(self, t, skier, schedule):
        if self.next_lift is not None:
            self.next_lift.handle_arrival(t, skier, schedule)
        else:
            # skier leaves resort; you can store exit time on skier if you want
            pass


class lift:
    def __init__(self, incoming_runs: List[run], outgoing_runs: List[run], capacity: int, speed: float):
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
    def choose_run(self):
        # first get array of weights
        weights = []
        weight_sum = 0
        for ski_run in self.outgoing_runs:   # outgoing_runs is your list of Run objects
            weight = ski_run.chance_to_take
            weights.append(weight)
            weight_sum += weight

        # error check
        if (len(weights) != len(self.outgoing_runs)) or weight_sum != 1:
            return None

        # make choice
        run_choice = np.random.choice(self.outgoing_runs, p=weights) # type: run
        return run_choice

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

        run = self.choose_run()
        # need some error handling here
        run.handle_run_start(t, skier, schedule)

        if self.queue:
            self._start_service(t, schedule)
    