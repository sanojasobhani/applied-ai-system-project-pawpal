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
