from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import time


@dataclass
class Task:
	title: str
	category: str
	duration: int  # minutes
	priority: int = 1
	preferred_time: Optional[time] = None
	recurrence: Optional[str] = None
	status: str = "pending"
	notes: Optional[str] = None
	pet_name: Optional[str] = None

	def mark_complete(self) -> None:
		self.status = "completed"

	def reschedule(self, new_time: time) -> None:
		self.preferred_time = new_time

	def conflicts_with(self, other: "Task") -> bool:
		# Scheduling conflict logic depends on assigned times; stub for now
		return False

	def priority_score(self) -> int:
		return int(self.priority)


@dataclass
class Pet:
	name: str
	species: str
	age: int
	health_notes: Optional[str] = None
	needs: List[str] = field(default_factory=list)

	def add_need(self, need: str) -> None:
		self.needs.append(need)

	def update_health_notes(self, notes: str) -> None:
		self.health_notes = notes

	def daily_requirements(self) -> List[str]:
		return list(self.needs)


class Owner:
	def __init__(self, name: str, contact_info: Optional[str] = None, availability: Optional[Dict[str, Any]] = None):
		self.name = name
		self.contact_info = contact_info
		self.availability = availability or {}
		self.pets: List[Pet] = []

	def set_availability(self, availability: Dict[str, Any]) -> None:
		self.availability = availability

	def set_preference(self, key: str, value: Any) -> None:
		prefs = self.availability.setdefault("preferences", {})
		prefs[key] = value

	def can_schedule(self, task_time: time) -> bool:
		# Simple placeholder: honor more sophisticated rules later
		return True

	def add_pet(self, pet: Pet) -> None:
		self.pets.append(pet)


class Scheduler:
	def __init__(self, owner: Owner, tasks: Optional[List[Task]] = None, constraints: Optional[Dict[str, Any]] = None):
		self.owner = owner
		self.tasks: List[Task] = tasks or []
		self.constraints = constraints or {}

	def add_task(self, task: Task) -> None:
		self.tasks.append(task)

	def sort_tasks(self) -> List[Task]:
		return sorted(self.tasks, key=lambda t: t.priority, reverse=True)

	def filter_tasks(self) -> List[Task]:
		return [t for t in self.tasks if t.status != "completed"]

	def resolve_conflicts(self, tasks: List[Task]) -> List[Task]:
		# Placeholder: naive implementation that assumes no conflicts
		return tasks

	def generate_plan(self) -> List[Task]:
		tasks = self.filter_tasks()
		tasks = self.sort_tasks()
		tasks = self.resolve_conflicts(tasks)
		return tasks

	def explain_plan(self, plan: List[Task]) -> str:
		titles = ", ".join(t.title for t in plan)
		return f"Plan ordered by priority: {titles}"


if __name__ == "__main__":
	owner = Owner("Alex", contact_info="alex@example.com")
	pet = Pet("Biscuit", "Dog", 5)
	owner.add_pet(pet)

	t1 = Task("Morning walk", "walk", 30, priority=5, pet_name=pet.name)
	t2 = Task("Feeding", "feeding", 10, priority=4, pet_name=pet.name)

	scheduler = Scheduler(owner, tasks=[t2, t1])
	plan = scheduler.generate_plan()
	print(scheduler.explain_plan(plan))
	for t in plan:
		print(f"- {t.title} ({t.duration}m) [priority {t.priority}]")

