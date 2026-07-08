# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

A user should be able to add pets, schedule walks, add medications and appointments, atc. Classes I made:

- Owner:
    - attributes: name, contact_info, available_hours, pets
    - methods: set_availability(), set_preference(), can_schedule(task_time), add_pet()
- Pet:
    - attributes: name, species, age, health_notes, needs
    - methods: add_need(), update_health_notes(), daily_requirements()
- Task:
    - attributes: title, category, duration, priority, preferred_time, recurrence, status, notes
    - methods: mark_complete(), reschedule(), conflicts_with(other_task), priority_score()
- Scheduler: 
    - attributes: owner, tasks, constraints
    - methods: generate_plan(), sort_tasks(), filter_tasks(), resolve_conflicts(), explain_plan()

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    Yes, I changed the way pet names were implemented to be a specific id to every pet, and I ensured tasks were connected to both pets and owners. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

constraints: time windows, priority, deadlines, reuccurence, pet-specific needs, owner preferences, and conflicts. Safety and simplicity were some of my highest priorities, and i prioritized constraints that could be practically addressed.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    Current conflict check detects exact ocerlaps and not partial overlaps.
- Why is that tradeoff reasonable for this scenario?
    its reasonable because the app is a lightweight pet care planner and not a full calendar, and a simple overlap checl keeps the code fast and easy.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used ai to help me run tests and build code, as well as to brainstorm app designs and key considerations. I also used ai to help me solve some issues with git.
- What kinds of prompts or questions were most helpful?
    Prompts that were direct and detailed were the most helpful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    During the initial design process, I used ai to help brainstorm objects but greatly refined the suggestions.
- How did you evaluate or verify what the AI suggested?
    AI was suggesting many unecessary classes, so I refined and cut down on classes to ensure the app was practical and reasonable.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    scheduling, conflict detection, reuccurence, availibility, and preferences
- Why were these tests important?
    these were important because they ensured a more seamless user experience that prevented double booking, constantly having to add the same weekly task, and ensured pet safety.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    I'm fairly confident, I tested many of the features and tested several edge cases as well.
- What edge cases would you test next if you had more time?
    Partial overlaps, recurrence more complex than just every week, time-zones, and daylight savings.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am satisfied with my app code as a basic framework. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would continue to improve on the schedule conflict checking method to check partial overlaps.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned that AI can be a powerful tool and should be utilized to its full extent as a builder rather than just a debugger.