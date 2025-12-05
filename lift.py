from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from event import Event
import numpy as np

if TYPE_CHECKING:
    from run import Run
    from skier import Skier


class Lift:
    def __init__(self, name: str, incoming_runs: list[Run], outgoing_runs: list[Run], capacity: int, speed: float):
        self.name = name
        self.lift_capacity = capacity
        self.lift_speed = speed # How long it takes to ride the lift - in minutes
        self.lift_wait_time: float = 0 # Wait for a lift to arrive + pick people up - in minutes
        self.incoming_runs: list[Run] = incoming_runs
        self.outgoing_runs: list[Run] = outgoing_runs

        self.queue: list[Skier] = []
        self.skiers_in_service: list[Skier] = []

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

    def handle_arrival(self, current_time: float, skier: Skier, schedule: Callable[[Event], None]) -> None:
        skier.enter_queue(current_time)  # Track when skier enters queue
        self.queue.append(skier)

        if len(self.skiers_in_service) == 0:
            # No one is currently on the lift
            self.start_service(current_time, schedule)

    def start_service(self, current_time: float, schedule: Callable[[Event], None]) -> None:
        # Serves multiple skiers at once (up to capacity)
        if not self.queue:
            print(f"Error: No skiers in queue to start lift {self.name}")
            return
        
        # Load multiple skiers onto the lift at once
        num_to_load = min(self.lift_capacity, len(self.queue))
        for _ in range(num_to_load):
            skier = self.queue.pop(0)
            self.skiers_in_service.append(skier)
            skier.start_lift(current_time)  # Track when skier starts lift ride


        # Schedule a single depart event for all skiers on the lift
        depart_time = current_time + self.lift_speed
        schedule(Event(depart_time, Event.EventType.LIFT_DEPART, self, None))

    def handle_departure(self, current_time: float, schedule: Callable[[Event], None]) -> None:
        # Depart all skiers currently on the lift
        departing_skiers = self.skiers_in_service.copy()
        self.skiers_in_service.clear()
        
        # Each skier chooses their own run and starts skiing
        for skier in departing_skiers:
            skier.finish_lift(current_time)  # Track when skier finishes lift ride
            
            run = self.choose_run()
            if run is None:
                print("Error: No run chosen from lift")
                continue
            
            run.handle_run_start(current_time, skier, schedule)
        
        # If there are skiers waiting, start the next lift ride
        if self.queue:
            self.start_service(current_time, schedule)
    