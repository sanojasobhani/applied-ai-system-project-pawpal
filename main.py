from datetime import datetime, time

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner("Alex", contact_info="alex@example.com")
    owner.set_availability({"start": time(7, 0), "end": time(21, 0)})

    pet1 = Pet(name="Biscuit", species="Dog", age=5)
    pet2 = Pet(name="Mittens", species="Cat", age=3)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    tasks = [
        Task(
            title="Give Mittens medication",
            category="medication",
            duration=15,
            priority=5,
            pet_id=pet2.id,
            preferred_time=time(10, 0),
        ),
        Task(
            title="Feed Biscuit",
            category="feeding",
            duration=10,
            priority=4,
            pet_id=pet1.id,
            preferred_time=time(9, 0),
        ),
        Task(
            title="Morning walk",
            category="walk",
            duration=30,
            priority=5,
            pet_id=pet1.id,
            preferred_time=time(8, 0),
        ),
        Task(
            title="Play session",
            category="play",
            duration=30,
            priority=3,
            pet_id=pet2.id,
            preferred_time=time(8, 0),
        ),
    ]

    scheduler = Scheduler(owner, tasks=tasks)
    plan = scheduler.generate_plan(start_dt=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0))

    print("Today's Schedule")
    print("-----------------")
    for task in plan:
        pet = owner.get_pet(task.pet_id) if task.pet_id else None
        pet_name = pet.name if pet else "Unknown pet"
        start_time = task.scheduled_start.strftime("%H:%M") if task.scheduled_start else "unscheduled"
        print(f"{start_time} — {task.title} ({task.category}) for {pet_name} [{task.duration} min]")

    print("\nFiltered pending tasks:")
    for task in scheduler.filter_tasks(completed=False):
        print(f"- {task.title} ({task.pet_name or 'unknown'})")

    print("\nSorted by time:")
    for task in scheduler.sort_by_time(plan):
        print(f"- {task.title} at {task.scheduled_start.strftime('%H:%M') if task.scheduled_start else 'unscheduled'}")

    overlap_a = Task(title="Overlapping check A", category="feeding", duration=20, priority=5, pet_name="Biscuit")
    overlap_b = Task(title="Overlapping check B", category="walk", duration=20, priority=5, pet_name="Mittens")
    overlap_a.scheduled_start = datetime(2024, 1, 1, 8, 0)
    overlap_a.scheduled_end = datetime(2024, 1, 1, 8, 20)
    overlap_b.scheduled_start = datetime(2024, 1, 1, 8, 0)
    overlap_b.scheduled_end = datetime(2024, 1, 1, 8, 20)

    print("\nConflict check:")
    print(scheduler.lightweight_conflict_check([overlap_a, overlap_b]))


if __name__ == "__main__":
    main()
