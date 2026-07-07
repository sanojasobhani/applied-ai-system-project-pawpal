import pytest
from pawpal_system import Pet, Task


def test_task_completion_changes_status():
    task = Task(title="Test task", category="feeding", duration=10)
    assert task.status == "pending"

    task.mark_complete()

    assert task.status == "completed"


def test_pet_task_addition_increases_count():
    pet = Pet(name="Biscuit", species="Dog", age=5)
    initial_count = pet.task_count()

    task = Task(title="Feed Biscuit", category="feeding", duration=10)
    pet.add_task(task)

    assert pet.task_count() == initial_count + 1
