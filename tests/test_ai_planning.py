from datetime import datetime, time

from pawpal_system import CareKnowledgeBase, Owner, Pet, PlanningAdvisor, Scheduler, Task


def test_retrieval_uses_relevant_guidance_for_medication_tasks():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)

    task = Task(title="Give medicine", category="medication", duration=10, priority=4, pet_name=pet.name)
    advisor = PlanningAdvisor(knowledge_base=CareKnowledgeBase())

    guidance = advisor.retrieve_guidance([task], owner)

    assert guidance
    assert any("medication" in item.lower() for item in guidance)


def test_ai_plan_report_scores_reliable_schedule():
    owner = Owner("Jordan")
    owner.set_availability({"start": time(7, 0), "end": time(20, 0)})

    feed_task = Task(
        title="Feed Mochi",
        category="feeding",
        duration=10,
        priority=4,
        pet_name="Mochi",
        preferred_time=time(8, 0),
    )
    walk_task = Task(
        title="Morning walk",
        category="walk",
        duration=30,
        priority=3,
        pet_name="Mochi",
        preferred_time=time(8, 0),
    )

    scheduler = Scheduler(owner, tasks=[feed_task, walk_task])
    result = scheduler.generate_plan_with_ai(start_dt=datetime(2024, 1, 1, 8, 0))

    assert result["plan"]
    assert result["guidance"]
    assert result["reliability"]["score"] >= 70
    assert result["reliability"]["status"] in {"good", "excellent"}


def test_time_of_day_keywords_infer_sensible_preferred_times():
    breakfast = Task(title="Breakfast", category="feeding", duration=10, priority=4, pet_name="Mochi")
    lunch = Task(title="Lunch", category="feeding", duration=10, priority=4, pet_name="Mochi")
    dinner = Task(title="Dinner", category="feeding", duration=10, priority=4, pet_name="Mochi")
    morning_walk = Task(title="Morning walk", category="walk", duration=30, priority=3, pet_name="Mochi")
    evening_walk = Task(title="Evening walk", category="walk", duration=30, priority=3, pet_name="Mochi")
    night_check = Task(title="Night check", category="general", duration=10, priority=2, pet_name="Mochi")

    assert breakfast.infer_time_preference() == time(7, 30)
    assert lunch.infer_time_preference() == time(12, 0)
    assert dinner.infer_time_preference() == time(18, 0)
    assert morning_walk.infer_time_preference() == time(8, 0)
    assert evening_walk.infer_time_preference() == time(18, 30)
    assert night_check.infer_time_preference() == time(21, 0)


def test_generate_plan_places_daypart_tasks_in_appropriate_windows():
    owner = Owner("Jordan")
    owner.set_availability({"start": time(7, 0), "end": time(23, 0)})

    morning_walk = Task(title="Morning walk", category="walk", duration=30, priority=3, pet_name="Mochi")
    lunch = Task(title="Lunch", category="feeding", duration=20, priority=4, pet_name="Mochi")
    dinner = Task(title="Dinner", category="feeding", duration=20, priority=4, pet_name="Mochi")
    night_check = Task(title="Night check", category="general", duration=15, priority=2, pet_name="Mochi")

    scheduler = Scheduler(owner, tasks=[lunch, dinner, night_check, morning_walk])
    plan = scheduler.generate_plan(start_dt=datetime(2024, 1, 1, 7, 0))

    scheduled_times = {task.title: task.scheduled_start.time() for task in plan}

    assert scheduled_times["Morning walk"].hour < 12
    assert 11 <= scheduled_times["Lunch"].hour <= 13
    assert 17 <= scheduled_times["Dinner"].hour <= 20
    assert scheduled_times["Night check"].hour >= 20
