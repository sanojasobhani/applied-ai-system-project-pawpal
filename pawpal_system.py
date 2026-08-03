from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from copy import deepcopy
from typing import Any, Dict, List, Optional
from uuid import uuid4


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
    pet_id: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None

    def mark_complete(self) -> None:
        self.status = "completed"

    def next_occurrence(self) -> "Task":
        if self.recurrence not in {"daily", "weekly"}:
            return self

        next_task = deepcopy(self)
        next_task.status = "pending"
        next_task.scheduled_start = None
        next_task.scheduled_end = None

        if self.recurrence == "daily" and self.scheduled_start and self.scheduled_end:
            next_task.scheduled_start = self.scheduled_start + timedelta(days=1)
            next_task.scheduled_end = self.scheduled_end + timedelta(days=1)
        elif self.recurrence == "weekly" and self.scheduled_start and self.scheduled_end:
            next_task.scheduled_start = self.scheduled_start + timedelta(weeks=1)
            next_task.scheduled_end = self.scheduled_end + timedelta(weeks=1)

        next_task.preferred_time = self.preferred_time
        return next_task

    def reschedule(self, new_time: time) -> None:
        self.preferred_time = new_time

    def conflicts_with(self, other: "Task") -> bool:
        if not self.scheduled_start or not self.scheduled_end or not other.scheduled_start or not other.scheduled_end:
            return False
        return self.scheduled_start < other.scheduled_end and other.scheduled_start < self.scheduled_end

    def priority_score(self) -> int:
        score = int(self.priority)
        category_weights = {
            "feeding": 2,
            "medication": 3,
            "walk": 2,
            "grooming": 1,
            "play": 1,
            "general": 1,
        }
        score += category_weights.get(self.category.lower(), 0)
        if self.category.lower() in {"medication", "feeding"}:
            score += 1
        if self.pet_name:
            score += 1
        if self.preferred_time is not None:
            score += 1
        return score


@dataclass
class Pet:
    name: str
    species: str
    age: int
    id: str = field(default_factory=lambda: str(uuid4()))
    health_notes: Optional[str] = None
    needs: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_need(self, need: str) -> None:
        self.needs.append(need)

    def update_health_notes(self, notes: str) -> None:
        self.health_notes = notes

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def task_count(self) -> int:
        return len(self.tasks)

    def daily_requirements(self) -> List[str]:
        return list(self.needs)


class CareKnowledgeBase:
    def __init__(self, entries: Optional[List[Dict[str, Any]]] = None):
        self.entries = entries or [
            {
                "category": "medication",
                "guidance": "Medication tasks should be scheduled early because they are time-sensitive and important for pet health.",
            },
            {
                "category": "feeding",
                "guidance": "Feeding tasks should be placed before long activities so the pet routine stays consistent.",
            },
            {
                "category": "walk",
                "guidance": "Walks fit well after feeding or before rest, and should avoid conflicting with urgent care tasks.",
            },
            {
                "category": "play",
                "guidance": "Play sessions work best after essential care work is completed and can be used as a reward block.",
            },
            {
                "category": "grooming",
                "guidance": "Grooming tasks are easier when the pet is calm and the day’s high-priority care tasks are already planned.",
            },
        ]

    def retrieve(self, tasks: List[Task], owner: Optional["Owner"] = None) -> List[str]:
        guidance: List[str] = []
        seen = set()

        for task in tasks:
            category = (task.category or "").lower()
            for entry in self.entries:
                if entry["category"] != category:
                    continue
                statement = entry["guidance"]
                if statement not in seen:
                    guidance.append(statement)
                    seen.add(statement)

        if owner and owner.pets:
            for pet in owner.pets:
                if pet.health_notes:
                    note = f"{pet.name} health note: {pet.health_notes}"
                    if note not in seen:
                        guidance.append(note)
                        seen.add(note)
                if pet.needs:
                    need_note = f"{pet.name} special needs: {', '.join(pet.needs)}"
                    if need_note not in seen:
                        guidance.append(need_note)
                        seen.add(need_note)

        return guidance


class PlanningAdvisor:
    def __init__(self, knowledge_base: Optional[CareKnowledgeBase] = None):
        self.knowledge_base = knowledge_base or CareKnowledgeBase()

    def retrieve_guidance(self, tasks: List[Task], owner: Optional["Owner"] = None) -> List[str]:
        return self.knowledge_base.retrieve(tasks, owner)


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

    def can_schedule(self, task_time: Any) -> bool:
        if not self.availability:
            return True

        availability_start = self.availability.get("start")
        availability_end = self.availability.get("end")
        if not availability_start or not availability_end:
            return True

        if isinstance(task_time, datetime):
            candidate_time = task_time.time()
        else:
            candidate_time = task_time

        return availability_start <= candidate_time <= availability_end

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_pet(self, pet_id: Optional[str]) -> Optional[Pet]:
        if not pet_id:
            return None
        for pet in self.pets:
            if pet.id == pet_id:
                return pet
        return None


class Scheduler:
    def __init__(self, owner: Owner, tasks: Optional[List[Task]] = None, constraints: Optional[Dict[str, Any]] = None):
        self.owner = owner
        self.tasks: List[Task] = tasks or []
        self.constraints = constraints or {}
        self.buffer_minutes = int(self.constraints.get("buffer_minutes", 5))

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def mark_task_complete(self, task: Task) -> Task:
        """Mark a task complete and create the next recurring instance when needed."""
        task.mark_complete()
        if task.recurrence in {"daily", "weekly"}:
            next_task = task.next_occurrence()
            self.tasks.append(next_task)
            return next_task
        return task

    def sort_tasks(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        pending_tasks = tasks or self.filter_tasks()
        return sorted(
            pending_tasks,
            key=lambda t: (
                -t.priority_score(),
                t.preferred_time is None,
                t.preferred_time or time.max,
            ),
        )

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks ordered by their scheduled or preferred start time."""
        pending_tasks = tasks or self.filter_tasks()
        return sorted(
            pending_tasks,
            key=lambda t: (
                t.scheduled_start or datetime.combine(datetime.now().date(), t.preferred_time or time(23, 59)),
                t.preferred_time or time(23, 59),
            ),
        )

    def filter_tasks(self, *, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name."""
        tasks = self.tasks

        if completed is not None:
            tasks = [t for t in tasks if (t.status == "completed") is completed]

        if pet_name is not None:
            tasks = [t for t in tasks if (t.pet_name or "").lower() == pet_name.lower()]

        return tasks

    def detect_overlaps(self, tasks: Optional[List[Task]] = None) -> List[tuple[Task, Task]]:
        """Find pairs of tasks whose scheduled time windows overlap."""
        pending_tasks = tasks or self.tasks
        overlaps: List[tuple[Task, Task]] = []

        for index, first in enumerate(pending_tasks):
            for second in pending_tasks[index + 1 :]:
                if not first.scheduled_start or not first.scheduled_end or not second.scheduled_start or not second.scheduled_end:
                    continue
                if first.conflicts_with(second):
                    overlaps.append((first, second))

        return overlaps

    def lightweight_conflict_check(self, tasks: Optional[List[Task]] = None) -> str:
        """Return a safe warning message when overlapping tasks are detected."""
        try:
            overlaps = self.detect_overlaps(tasks)
            if not overlaps:
                return "No conflicts detected."
            conflict_summary = ", ".join(
                f"{first.title} overlaps with {second.title}" for first, second in overlaps
            )
            return f"Warning: possible scheduling conflict(s) detected — {conflict_summary}."
        except Exception:
            return "Warning: conflict check could not be completed safely."

    def resolve_conflicts(self, tasks: List[Task], start_dt: Optional[datetime] = None) -> List[Task]:
        if not tasks:
            return []

        base_time = start_dt or datetime.now().replace(second=0, microsecond=0)
        current_time = base_time
        planned: List[Task] = []
        availability_start = self.owner.availability.get("start")
        availability_end = self.owner.availability.get("end")

        for task in tasks:
            candidate_start = self._calculate_candidate_start(task, current_time, base_time)
            while self._has_conflict(candidate_start, task.duration, planned):
                candidate_start += timedelta(minutes=1)

            if availability_start and availability_end:
                while not self.owner.can_schedule(candidate_start):
                    candidate_start = datetime.combine(candidate_start.date() + timedelta(days=1), availability_start)

            task.scheduled_start = candidate_start
            task.scheduled_end = candidate_start + timedelta(minutes=task.duration)
            planned.append(task)
            current_time = task.scheduled_end + timedelta(minutes=self.buffer_minutes)

        return planned

    def _calculate_candidate_start(self, task: Task, current_time: datetime, base_time: datetime) -> datetime:
        if task.preferred_time is not None:
            preferred_start = datetime.combine(base_time.date(), task.preferred_time)
            if preferred_start < current_time:
                return current_time
            return preferred_start
        return current_time

    def _has_conflict(self, candidate_start: datetime, duration: int, planned: List[Task]) -> bool:
        candidate_end = candidate_start + timedelta(minutes=duration)
        for existing in planned:
            if existing.scheduled_start and existing.scheduled_end:
                if candidate_start < existing.scheduled_end and existing.scheduled_start < candidate_end:
                    return True
        return False

    def generate_plan(self, start_dt: Optional[datetime] = None) -> List[Task]:
        tasks = self.filter_tasks()
        tasks = self.sort_tasks(tasks)
        tasks = self.resolve_conflicts(tasks, start_dt=start_dt)
        return self.sort_by_time(tasks)

    def generate_plan_with_ai(
        self,
        start_dt: Optional[datetime] = None,
        knowledge_base: Optional[CareKnowledgeBase] = None,
    ) -> Dict[str, Any]:
        plan = self.generate_plan(start_dt=start_dt)
        advisor = PlanningAdvisor(knowledge_base=knowledge_base)
        guidance = advisor.retrieve_guidance(plan, self.owner)
        reliability = self._evaluate_plan_reliability(plan, guidance)
        return {"plan": plan, "guidance": guidance, "reliability": reliability}

    def _evaluate_plan_reliability(self, plan: List[Task], guidance: List[str]) -> Dict[str, Any]:
        score = 60
        notes = []

        if plan:
            score += 10
            notes.append("The scheduler produced a concrete plan.")
        if all(task.scheduled_start and task.scheduled_end for task in plan):
            score += 10
            notes.append("Every task was assigned a scheduled window.")
        if not self.detect_overlaps(plan):
            score += 10
            notes.append("The plan avoids scheduling conflicts.")
        if guidance:
            score += 10
            notes.append("Relevant pet-care guidance was retrieved and applied.")

        if score >= 90:
            status = "excellent"
        elif score >= 70:
            status = "good"
        else:
            status = "needs-attention"

        return {"score": min(score, 100), "status": status, "notes": " ".join(notes)}

    def explain_plan(self, plan: List[Task]) -> str:
        if not plan:
            return "No tasks are available to schedule today."

        reasons = []
        for index, task in enumerate(plan, start=1):
            score = task.priority_score()
            slot = task.scheduled_start.strftime("%H:%M") if task.scheduled_start else "unscheduled"
            reason = f"{index}. {task.title} was placed at {slot} because it scored {score} and was ordered ahead of lower-priority work."
            if task.preferred_time is not None:
                reason += f" It also matched the preferred time of {task.preferred_time.strftime('%H:%M')}."
            if task.category.lower() in {"medication", "feeding"}:
                reason += " This is a high-importance care task."
            reasons.append(reason)

        return " ".join(reasons)


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

