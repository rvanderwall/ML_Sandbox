import unittest
from parameterized import parameterized

DAYS_PER_WEEK = 7


class DayOfWeek:
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @staticmethod
    def next_day(day: int):
        if day >= DayOfWeek.SUNDAY:
            return DayOfWeek.MONDAY
        else:
            return day + 1


class Task:
    def __init__(self):
        self.duration_hours = 0
        self.start_day = DayOfWeek.MONDAY
        self.start_time = 0


class JiraSim:
    def __init__(self, hours_per_day, workdays_per_week):
        self.hours_per_day = hours_per_day
        self.workdays_per_week = workdays_per_week

        self.weekend_days = DAYS_PER_WEEK - self.workdays_per_week

    def how_long_for_task(self, task: Task):
        # No work on weekends.
        if task.start_day > self.workdays_per_week:
            task.start_time = 0
            task.start_day = DayOfWeek.next_day(task.start_day)
            return 1 + self.how_long_for_task(task)

        hours_left_in_today = self.hours_per_day - task.start_time

        # We can finish task today, 1 day duration
        if task.duration_hours <= hours_left_in_today:
            return 1

        task.duration_hours = task.duration_hours - hours_left_in_today
        task.start_time = 0
        task.start_day = DayOfWeek.next_day(task.start_day)
        return 1 + self.how_long_for_task(task)

    def sim_week(self, task_duration):
        days = 0
        cum_days = 0
        for day in range(1, self.workdays_per_week+1):
            t = Task()
            t.start_time = 0
            t.duration_hours = task_duration
            t.start_day = day
            days += 1
            cum_days += self.how_long_for_task(t)

        ave_latency = cum_days / days
        return ave_latency


def run_sim():
    print(f"Task size, 10Hr day latency,8hr day latency")
    for task_size in range(1, 200):
        sim = JiraSim(10, 4)
        l1 = sim.sim_week(task_size)
        sim = JiraSim(8, 5)
        l2 = sim.sim_week(task_size)
        print(f"{task_size},{l1},{l2}")
        # print(f"Task size:{task_size}, 10Hr day latency:{l1}  8hr day latency:{l2}")

class JiraSimTests(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.sim = JiraSim(10, 4)

    @parameterized.expand([
        (DayOfWeek.MONDAY, 1),
        (DayOfWeek.THURSDAY, 1),
    ])
    def test_one_hour_task_workday(self, start_day, expected_duration):
        t = Task()
        t.start_time = 1
        t.duration_hours = 1
        t.start_day = start_day

        days = self.sim.how_long_for_task(t)

        self.assertEqual(expected_duration, days)

    @parameterized.expand([
        (DayOfWeek.FRIDAY, 4),
        (DayOfWeek.SATURDAY, 3),
        (DayOfWeek.SUNDAY, 2),
    ])
    def test_one_hour_task_on_weekend(self, start_day, expected_duration):
        t = Task()
        t.start_time = 1
        t.duration_hours = 1
        t.start_day = start_day

        days = self.sim.how_long_for_task(t)

        self.assertEqual(expected_duration, days)

    @parameterized.expand([
        (DayOfWeek.MONDAY, 2),
        (DayOfWeek.TUESDAY, 2),
        (DayOfWeek.THURSDAY, 5),  # TFSSM
        (DayOfWeek.FRIDAY, 4),    # FSSM
        (DayOfWeek.SUNDAY, 2),  # FSSM
    ])
    def test_multihour_task(self, start_day, expected_days):
        t = Task()
        t.duration_hours = 4
        t.start_time = 9    # We have only 1 hour left in the first day
        t.start_day = start_day

        days = self.sim.how_long_for_task(t)

        self.assertEqual(expected_days, days)

    @parameterized.expand([
        (DayOfWeek.MONDAY, 2),
        (DayOfWeek.TUESDAY, 2),
        (DayOfWeek.THURSDAY, 5),  # TFSSM
        (DayOfWeek.FRIDAY, 5),    # FSSM
        (DayOfWeek.SUNDAY, 3),  # FSSM
    ])
    def test_multiday_task(self, start_day, expected_days):
        t = Task()
        t.duration_hours = 15
        t.start_time = 5    # We have 5 hour left in the first day
        t.start_day = start_day

        days = self.sim.how_long_for_task(t)

        self.assertEqual(expected_days, days)
