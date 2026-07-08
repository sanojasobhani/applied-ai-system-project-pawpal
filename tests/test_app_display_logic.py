from datetime import datetime

from app import get_conflict_warning, get_sorted_task_rows
from pawpal_system import Owner, Scheduler, Task


def test_get_sorted_task_rows_uses_scheduler_priority_order():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)

    low_priority_task = Task(title="Low task", category="general", duration=10, priority=1, pet_name="Mochi")
    high_priority_task = Task(title="High task", category="medication", duration=10, priority=3, pet_name="Mochi")
    scheduler.add_task(low_priority_task)
    scheduler.add_task(high_priority_task)

    rows = get_sorted_task_rows(scheduler, scheduler.tasks)

    assert [row["title"] for row in rows] == ["High task", "Low task"]


def test_get_conflict_warning_uses_scheduler_conflict_detection():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)

    first = Task(title="Feed Mochi", category="feeding", duration=20, pet_name="Mochi")
    second = Task(title="Walk Mochi", category="walk", duration=20, pet_name="Mochi")

    first.scheduled_start = datetime(2024, 1, 1, 8, 0)
    first.scheduled_end = datetime(2024, 1, 1, 8, 20)
    second.scheduled_start = datetime(2024, 1, 1, 8, 10)
    second.scheduled_end = datetime(2024, 1, 1, 8, 30)

    message = get_conflict_warning(scheduler, [first, second])

    assert "Warning" in message
    assert "overlaps" in message
