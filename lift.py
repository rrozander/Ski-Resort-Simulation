from __future__ import annotations
from typing import TYPE_CHECKING
from event import Event
import numpy as np

if TYPE_CHECKING:
    from run import Run


class Lift:
    def __init__(self, incoming_runs: list[Run], outgoing_runs: list[Run], capacity: int, speed: float):
        self.lift_capacity = capacity
        self.lift_speed = speed # How long it takes to ride the lift - in minutes
        self.lift_wait_time: float = 0 # Wait for a lift to arrive + pick people up - in minutes
        self.incoming_runs: list[Run] = incoming_runs
        self.outgoing_runs: list[Run] = outgoing_runs

        self.queue = []
        self.in_service = None

    
    def get_outgoing_runs(self):
        pass
    
    def get_incoming_runs(self):
        pass

    # need a function to choose next run
    def choose_run(self) -> Run | None:
        # first get array of weights
        weights = []
        weight_sum = 0
        for ski_run in self.outgoing_runs:   # outgoing_runs is your list of Run objects
            weight = ski_run.percentage_traffic
            weights.append(weight)
            weight_sum += weight

        # error check
        if (len(weights) != len(self.outgoing_runs)) or weight_sum != 1:
            return None

        # make choice
        run_choice = np.random.choice(self.outgoing_runs, p=weights)
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
        schedule(Event(depart_time, Event.EventType.LIFT_DEPART, self, None))

    def handle_departure(self, t, schedule,):
        skier = self.in_service
        self.in_service = None

        run = self.choose_run()
        # need some error handling here
        run.handle_run_start(t, skier, schedule)

        if self.queue:
            self._start_service(t, schedule)
    