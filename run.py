from __future__ import annotations
from typing import TYPE_CHECKING
from event import Event

if TYPE_CHECKING:
    from lift import Lift
    from skier import Skier

class Run:
    def __init__(self, name: str, avg_time: float, chance_to_take: float):
        self.name = name
        self.avg_run_time = avg_time # average time to complete the run - in minutes
        self.percentage_traffic = chance_to_take
        self.next_lift: Lift | None = None

    def handle_run_start(self, current_time: float, skier: Skier, schedule: callable) -> None:
        if self.avg_run_time <= 0:
            # Exiting Resort Run
            self.handle_run_finish(current_time, skier, schedule)
            return
        run_time = Event.generateInterArrival(self.avg_run_time)
        print(f"Skier {skier.id} starting run {self.name} at {current_time:.2f} minutes for estimated {run_time:.2f} minutes")
        finish_time = current_time + run_time
        schedule(Event(finish_time, Event.EventType.RUN_FINISH, self, skier))

    def handle_run_finish(self, current_time: float, skier: Skier, schedule: callable) -> None:
        if self.next_lift is not None:
            print(f"Skier {skier.id} finishing run {self.name} at {current_time:.2f} minutes")
            self.next_lift.handle_arrival(current_time, skier, schedule)
        else:
            # skier leaves resort; you can store exit time on skier if you want
            print(f"Skier {skier.id} exits resort at {current_time:.2f} minutes")
            pass
