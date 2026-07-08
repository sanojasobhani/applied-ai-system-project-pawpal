from datetime import datetime

import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value=st.session_state.get("owner_name", "Jordan"), key="owner_name")
pet_name = st.text_input("Pet name", value=st.session_state.get("pet_name", "Mochi"), key="pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], key="species")
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=3, step=1, key="pet_age")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler
owner.name = owner_name

st.markdown("### Add a Pet")
if st.button("Add pet", key="add_pet_button"):
    pet = Pet(name=pet_name, species=species, age=int(pet_age))
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(f"Added {pet.name} to {owner.name}'s profile.")

if owner.pets:
    st.write("Current pets:")
    pet_rows = [{"name": pet.name, "species": pet.species, "age": pet.age} for pet in owner.pets]
    st.table(pet_rows)
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Create tasks that the scheduler can order for your pet care plan.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority")

if st.button("Add task", key="add_task_button"):
    priority_map = {"low": 1, "medium": 2, "high": 3}
    task = Task(
        title=task_title,
        category="general",
        duration=int(duration),
        priority=priority_map[priority],
        pet_name=pet_name,
    )
    scheduler.add_task(task)
    st.session_state.scheduler = scheduler
    st.success(f"Added task: {task.title}")

if scheduler.tasks:
    st.write("Current tasks:")
    task_rows = [
        {
            "title": task.title,
            "duration": task.duration,
            "priority": task.priority,
            "pet": task.pet_name or "",
        }
        for task in scheduler.tasks
    ]
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a priority-based plan from the tasks you added.")

if st.button("Generate schedule", key="generate_schedule_button"):
    plan = scheduler.generate_plan(start_dt=datetime.now().replace(second=0, microsecond=0))
    explanation = scheduler.explain_plan(plan)
    st.success(explanation)

    if plan:
        st.write("Planned tasks:")
        plan_rows = [
            {
                "title": task.title,
                "start": task.scheduled_start.strftime("%H:%M") if task.scheduled_start else "unscheduled",
                "end": task.scheduled_end.strftime("%H:%M") if task.scheduled_end else "unscheduled",
                "duration": task.duration,
                "priority": task.priority,
            }
            for task in plan
        ]
        st.table(plan_rows)
    else:
        st.info("No tasks available to schedule yet.")
