# Model Card: PawPal+ Applied AI System

## Purpose
PawPal+ is a small applied AI system that helps turn pet-care tasks into a daily schedule. Its purpose is to support planning and decision-making for pet owners, not to replace veterinary or caregiving judgment.

## Limitations and Biases
The system has several important limitations. First, it relies on a lightweight knowledge base rather than a large external model, so its guidance is narrow and rule-based. Second, it may reflect the assumptions built into its task categories and priorities, such as treating medication and feeding as more urgent than leisure activities. Third, it does not understand the full context of a real pet’s health, behavior, or owner constraints beyond the information provided by the user.

Because of this, the system can be biased toward generic care priorities and may not fit every household situation. It should be used as a planning aid, not as a definitive medical or behavioral recommendation.

## Potential Misuse and Prevention
This AI could be misused if someone trusted it too much for health-sensitive decisions or used it to automate care without checking the actual needs of the pet. It could also be misused to over-schedule a pet’s day, creating unnecessary stress or ignoring important context.

To prevent misuse, the system should clearly present its recommendations as suggestions rather than absolute facts. The interface should encourage human review, especially for medication, medical care, and unusual behavior. The project also includes a reliability score and explanation output so that users can see when the system is confident and when the plan needs closer scrutiny.

## What Surprised Me During Testing
One surprising result was that the reliability score improved when the plan had clear, conflict-free structure and retrieved guidance. That showed that simple checks can make the system feel more trustworthy even without a large AI model. Another surprise was that the system behaved differently depending on the category labels used for tasks, which showed how sensitive planning logic can be to the quality of input data.

## Collaboration with AI During This Project
My collaboration with AI during this project was mostly iterative. I used AI to help structure the system, turn the original scheduling project into an applied AI workflow, and generate tests and documentation. This helped me move faster while still keeping the project grounded in the code I was building.

One helpful suggestion was when the AI proposed adding a reliability score and explanation output to the scheduling flow. That was useful because it made the system more transparent and gave the app a clear way to justify its output.

One flawed suggestion was when the AI initially suggested treating the system as if it were using a fully external generative model. That was not accurate for this project, because the implementation uses a lightweight knowledge base and rules-based planning. The suggestion was flawed because it overstated the system’s capabilities and did not match the actual architecture.

## Responsible Use Summary
This project demonstrates that AI can be useful in practical systems when it is paired with testing, explanation, and human review. The most responsible version of the system is one that makes its limits visible, scores its own reliability, and leaves final decisions to the user when the stakes are high.
