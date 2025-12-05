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
        self.lift_wait_time: float = 0.5 # Wait for a lift to arrive + pick people up - in minutes <- chair every 30 sec
        self.incoming_runs: list[Run] = incoming_runs
        self.outgoing_runs: list[Run] = outgoing_runs

        self.queue: list[Skier] = []
        self.skiers_in_service: list[list[Skier]] = [] # Each element is a group of skiers on a chair

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
            print("Error: Weights do not sum to 1 or length mismatch")
            print(f"Weights: {weights}, Sum: {weight_sum}, Outgoing runs: {len(self.outgoing_runs)}")
            return None

        # make choice
        run_choice = np.random.choice(self.outgoing_runs, p=weights)
        return run_choice

    def handle_arrival(self, current_time: float, skier: Skier, schedule: Callable[[Event], None]) -> None:
        skier.enter_queue(current_time)  # Track when skier enters queue
        self.queue.append(skier)

        if len(self.skiers_in_service) == 0:
            # No one is currently on the lift, schedule the next chair to arrive
            service_time = current_time + self.lift_wait_time
            schedule(Event(service_time, Event.EventType.LIFT_START, self, None))

    def start_service(self, current_time: float, schedule: Callable[[Event], None]) -> None:
        # Serves multiple skiers at once (up to capacity)
        if not self.queue:
            # No skiers waiting, but don't schedule another chair yet
            return
        
        # Load multiple skiers onto the lift at once
        num_to_load = min(self.lift_capacity, len(self.queue))
        skiers_loaded = []
        for _ in range(num_to_load):
            skier = self.queue.pop(0)
            skiers_loaded.append(skier)
            skier.start_lift(current_time)  # Track when skier starts lift ride
        self.skiers_in_service.append(skiers_loaded)


        # Schedule a single depart event for all skiers on the lift
        depart_time = current_time + self.lift_speed
        schedule(Event(depart_time, Event.EventType.LIFT_DEPART, self, None))
        
        # Schedule the next chair to arrive after lift_wait_time
        next_chair_time = current_time + self.lift_wait_time
        schedule(Event(next_chair_time, Event.EventType.LIFT_START, self, None))

    def handle_departure(self, current_time: float, schedule: Callable[[Event], None]) -> None:
        # Depart all skiers currently on the lift
        departing_skiers = self.skiers_in_service.pop(0) # Remove the oldest group of skiers on the lift
        
        # Each skier chooses their own run and starts skiing
        for skier in departing_skiers:
            skier.finish_lift(current_time)  # Track when skier finishes lift ride
            
            run = self.choose_run()
            if run is None:
                print("Error: No run chosen from lift")
                continue
            
            run.handle_run_start(current_time, skier, schedule)
    