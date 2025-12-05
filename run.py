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
        self.dest_lift: Lift | None = None

    def handle_run_start(self, current_time: float, skier: Skier, schedule: callable) -> None:
        if self.avg_run_time <= 0:
            # Exiting Resort Run
            self.handle_run_finish(current_time, skier, schedule)
            return
        run_time = Event.generateInterArrival(self.avg_run_time)
        # print(f"Skier {skier.id} starting run {self.name} at {current_time:.2f} minutes for estimated {run_time:.2f} minutes")
        finish_time = current_time + run_time
        schedule(Event(finish_time, Event.EventType.RUN_FINISH, self, skier))

    def handle_run_finish(self, current_time: float, skier: Skier, schedule: callable) -> None:
        if self.dest_lift is not None:
            # print(f"Skier {skier.id} finishing run {self.name} at {current_time:.2f} minutes")
            self.dest_lift.handle_arrival(current_time, skier, schedule)
        else:
            # skier leaves resort
            skier.leave_resort(current_time)  # Track when skier leaves resort

            stats = skier.get_stats()
            # print(f"  Stats - Total time: {stats['total_time_at_resort']:.2f} min, Wait time: {stats['time_waiting_in_line']:.2f} min, Lift time: {stats['time_on_lift']:.2f} min")
