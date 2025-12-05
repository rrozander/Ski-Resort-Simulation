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

        self.queue = []
        self.skiers_in_service = None

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
        self.queue.append(skier)

        if self.skiers_in_service is None:
            # No one is in queue
            self.start_service(current_time, schedule)
        # else:
        #     # Skier need to wait in line
        #     # TODO: implement wait logic

        #     print(f"{self.name} Full")
        #     pass

    def start_service(self, current_time: float, schedule: Callable[[Event], None]) -> None:
        # Serves the next skier in line
        # TODO: Update this with the capacity logic
        if not self.queue:
            return
        self.skiers_in_service = self.queue.pop(0)
        print(f"{self.name} Serving Skier {self.skiers_in_service.id} at {current_time:.2f} minutes")
        depart_time = current_time + self.lift_speed
        schedule(Event(depart_time, Event.EventType.LIFT_DEPART, self, None))

    def handle_departure(self, current_time: float, schedule: Callable[[Event], None]) -> None:
        skier = self.skiers_in_service
        self.skiers_in_service = None

        print(f"{self.name} Departing Skier {skier.id} at {current_time:.2f} minutes")
        
        run = self.choose_run()
        if run is None:
            print("Error: No run chosen from lift")
            return

        run.handle_run_start(current_time, skier, schedule)

        if self.queue != []:
            self.start_service(current_time, schedule)
    