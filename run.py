from __future__ import annotations
from event import Event

class Run:
    def __init__(self, avg_time: float, chance_to_take: float):
        self.avg_run_time = avg_time # average time to complete the run - in minutes
        self.percentage_traffic = chance_to_take
        self.next_lift = None  # type: Lift | None

    def handle_run_start(self, t, skier, schedule):
        if self.avg_run_time <= 0:
            self.handle_run_finish(t, skier, schedule)
            return
        run_time = Event.generateInterArrival(self.avg_run_time)
        finish_time = t + run_time
        schedule(Event(finish_time, Event.EventType.RUN_FINISH, self, skier))

    def handle_run_finish(self, t, skier, schedule):
        if self.next_lift is not None:
            self.next_lift.handle_arrival(t, skier, schedule)
        else:
            # skier leaves resort; you can store exit time on skier if you want
            pass
