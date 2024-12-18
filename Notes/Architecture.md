
# CV Optimization LLM Project Architecture

## Introduction

This document provides an architecture for a dynamic, user-specific questionnaire for CV optimization using a **multi-agent system in LangGraph**. The system generates a tailored CV based on a provided job description (JD) and CV, utilizing an LLM-based approach to gather inputs from the candidate through dynamically generated questions.

---

## **System Architecture**

The multi-agent system consists of several agents interacting with each other and the candidate. LangGraph orchestrates the agent workflows to optimize the CV by filling in gaps identified through analysis of the candidate's CV and the job description.

### **Agents Involved**
1. **Critic Agent**  
   - **Role**: Analyzes the CV and JD, identifying missing keywords, skills, and providing critique with actionable insights.  
   - **Input**: CV, Job Description  
   - **Output**: Missing keywords (technical and non-technical), detailed critique, and a matching score out of 100.  

2. **Questionnaire Generation Agent**  
   - **Role**: Generates a dynamic, personalized questionnaire based on:  
     - Missing keywords  
     - Critique insights  
     - Current user responses  
   - **Input**: Critic Agent's output, user responses  
   - **Output**: A list of contextual questions.

3. **Candidate Response Agent**  
   - **Role**: Manages candidate inputs and stores responses. Dynamically validates and assesses answers to determine if they address identified gaps.  
   - **Input**: User responses  
   - **Output**: Structured responses fed back to other agents.  

4. **Skill Mapping Agent**  
   - **Role**: Matches the user responses to the missing technical and non-technical skills. Updates the system state based on progress.  
   - **Input**: Questionnaire answers from the Candidate Response Agent  
   - **Output**: Updated progress state (e.g., identified skills, validation of existing ones).

5. **Curated CV Generator Agent**  
   - **Role**: Combines insights from all agents (Critic, Questionnaire Generation, Skill Mapping) to produce a tailored CV.  
   - **Input**: Updated skill mappings, user responses, base CV  
   - **Output**: A revised, optimized CV matching the JD.

6. **State Management Agent**  
   - **Role**: Maintains and tracks the overall progress of the candidate.  
   - **Input**: Responses, questionnaire states, updated skills  
   - **Output**: State updates to dynamically adjust the flow.

---

## **System Flow Using LangGraph**

LangGraph enables building a graph-based multi-agent workflow. Below is the proposed flow of how the system will operate:

### 1. **Input Stage**  
   - The user provides the **base CV** and **Job Description**.  
   - The **Critic Agent** is triggered, generating missing keywords, critique, and a matching score.

### 2. **Dynamic Questionnaire Generation Loop**  
   - The **Questionnaire Generation Agent** analyzes the critique output and generates an initial dynamic questionnaire.  
   - Questions are based on missing technical/non-technical skills, ambiguous areas, or existing experiences.

### 3. **Candidate Response Interaction**  
   - The **Candidate Response Agent** interacts with the user, accepting responses. It feeds these responses back to:  
     - The **Questionnaire Generation Agent** to adjust subsequent questions.  
     - The **Skill Mapping Agent** to validate the skills and map them against the job requirements.

### 4. **Iterative Updates**  
   - The system dynamically adjusts its questioning based on user responses.  
     - If a response resolves a missing keyword, it's marked as addressed.  
     - If gaps remain, follow-up questions are triggered.  
     - If the candidate lacks specific skills, alternative questions are generated (e.g., willingness to learn or transferable skills).

### 5. **State Tracking**  
   - The **State Management Agent** tracks progress by maintaining a state machine.  
   - It manages nodes (e.g., addressed gaps, unresolved gaps) and ensures no redundant questioning.

### 6. **CV Curation**  
   - Once all relevant gaps are addressed, the **Curated CV Generator Agent** produces a tailored CV using the base CV and updated responses/skills.

### 7. **Final Output**  
   - The tailored CV is delivered to the user, accompanied by a summary of improvements and remaining gaps (if any).

---

## **Dynamic Questionnaire Generation Logic**

The questionnaire is designed to be dynamic and adaptive. Here's how it works:

### Initial Round
- Questions are seeded based on the critique output and missing skills. For example:  
  - **Technical Gap:** *“Do you have experience using X? If yes, please provide details.”*  
  - **Non-technical Gap:** *“Have you worked in cross-functional teams? Can you share an experience?”*  

### Adaptive Follow-up
- If the candidate answers affirmatively to a question, probe for specifics:  
  - *“Great! Can you share a project or result that demonstrates this skill?”*  
- If the answer is negative, explore alternatives:  
  - *“Do you have any related experience or transferable skills in this area?”*  
- If ambiguity remains, clarify further:  
  - *“Your CV mentions XYZ, but it doesn’t align fully with the requirement. Can you elaborate?”*

The **Skill Mapping Agent** tracks responses and validates the presence of missing skills.

---

## **Key Considerations for Architecture**

1. **State Management**:  
   Use LangGraph’s graph nodes to manage progress and state transitions (e.g., gaps resolved, unanswered questions).

2. **Prompt Chaining**:  
   Use modular prompts for each agent to ensure clean hand-offs and maintain context.

3. **Loop Control**:  
   Implement guardrails to avoid infinite questioning loops:  
   - Limit follow-ups per skill.  
   - Allow candidates to skip questions or mark them as irrelevant.

4. **User-Centric Design**:  
   Ensure that questions are concise, context-aware, and non-overwhelming to prevent user fatigue.

---

## **Example Graph Workflow**

```
[Input Stage] → [Critic Agent] → [Questionnaire Generation Agent] → 
    → [Candidate Response Agent] ↔ [Skill Mapping Agent] ↔ [State Management Agent]
    → [Curated CV Generator Agent] → [Output: Tailored CV]
```

### Nodes (Graph States):
- Critic Analysis
- Dynamic Question Generation
- User Response Collection
- Skill Validation
- CV Generation

### Edges (Transitions):
- Triggered by user responses, missing gaps, or updated states.

---

## **Why Multi-Agent LangGraph?**

LangGraph is an ideal platform for building this system because it allows you to:
1. Define **autonomous agents** for distinct tasks (analysis, questioning, response validation, CV generation).
2. Orchestrate agents in a **graph-based workflow**, enabling dynamic state transitions.
3. Maintain **context across agents** to ensure a cohesive experience.
4. Dynamically adjust questioning paths based on responses, achieving adaptiveness.

---

## **Next Steps**

1. **Define individual agents** with modular prompts for each task.
2. **Implement the state transitions** and agent communications using LangGraph.
3. **Test iteratively** with sample CVs and job descriptions to validate adaptiveness and correctness of the flow.

By combining **multi-agent collaboration** and **dynamic questioning**, you will have a robust, adaptive system capable of efficiently tailoring CVs to match job descriptions.
