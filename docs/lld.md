# Socra - Low Level Design (LLD)

## Section 1 — API Endpoints

**Base URL:** `https://api.socra.com/path`

### 1\. Create a New Session

**Method + URL:** `POST /v1/session`

**Description:** Creates a new session.

**Request Body:**

``` json
{
  "problem_text": "Given an array of Integers nums...."
}

```

**Response Body:**

``` json
{
  "session_id": "abc123",
  "content": "The problem mentions that….",
  "hint_level": 0,
  "session_status": "active"
}

```

**Possible Errors:**

  * **401 Unauthorized:** User is not logged into Socra.
  * **400 Bad Request:** Empty problem statement sent.
  * **503 Server Unavailable:** Excessive load causing server crash.

-----

### 2\. Send Message

**Method + URL:** `POST /v1/session/{id}/message`

**Description:** Sends a message and receives a response.

**Request Body:**

``` json
{
  "content": "How do I initialize the value of mid"
}

```

**Response Body:**

``` json
{
  "role": "coach",
  "content": "You have your left and right pointers at both ends of the array, and you have your mid, midway between the two",
  "hint_level": 2,
  "session_status": "active"
}

```

**Possible Errors:**

  * **404 Not Found:** Session ID missing in URL.
  * **401 Unauthorized:** Missing JWT in header.
  * **422 Unprocessable Entity:** Missing content field in request body.

-----

### 3\. Retrieve Session History

**Method + URL:** `GET /v1/session/{id}`

**Description:** Retrieves the session data of all exchanges.

**Request Body:**

``` json
{
  "request": "retrieve the entire conversation history of session abc123"
}

```

**Response Body:**

``` json
{
  "session_id": "abc123",
  "problem_text": "Given an array of integers...",
  "hint_level": 2,
  "session_status": "active",
  "messages": [
    {
      "role": "student",
      "content": "I'm stuck on the loop constraint."
    },
    {
      "role": "coach",
      "content": "What happens when your left pointer meets the right?"
    }
  ]
}

```

**Possible Errors:**

  * **401 Unauthorized:** Missing JWT in header.
  * **404 Not Found:** Session ID missing or does not exist.
  * **500 Internal Server Error:** Schema validation failure.

-----

## Section 2 — Database Schema

### Users Schema

| Column             | Data type   | Description        | Constraints             |
| :----------------- | :---------- | :----------------- | :---------------------- |
| **id**             | UUID        | Unique User ID     | PRIMARY KEY             |
| **name**           | VARCHAR(n)  | Name of the user   | NOT NULL                |
| **email**          | VARCHAR(n)  | Email address      | NOT NULL, UNIQUE        |
| **signup\_time**   | Time\_Stamp | Sign up time       | NOT NULL, DEFAULT NOW() |
| **auth\_provider** | VARCHAR(n)  | How they logged in | NOT NULL                |

### Sessions Schema

| Column Name              | Data Type   | Description                        | Constraints                                |
| :----------------------- | :---------- | :--------------------------------- | :----------------------------------------- |
| **id**                   | UUID        | Unique identifier                  | PRIMARY KEY                                |
| **user\_id**             | UUID        | Links to user                      | FOREIGN KEY REFERENCES users(id), NOT NULL |
| **problem\_text**        | TEXT        | LeetCode problem text              | NOT NULL                                   |
| **current\_hint\_level** | INTEGER     | Hint depth (1-5)                   | NOT NULL, DEFAULT 1                        |
| **status**               | VARCHAR(50) | State (active/completed/abandoned) | NOT NULL, DEFAULT 'active'                 |
| **created\_at**          | TIMESTAMP   | Creation time                      | NOT NULL, DEFAULT NOW()                    |

### Messages Schema

| Column Name         | Data Type   | Description          | Constraints                                   |
| :------------------ | :---------- | :------------------- | :-------------------------------------------- |
| **id**              | UUID        | Unique identifier    | PRIMARY KEY                                   |
| **session\_id**     | UUID        | Links to session     | FOREIGN KEY REFERENCES sessions(id), NOT NULL |
| **sender**          | VARCHAR(50) | 'student' or 'coach' | NOT NULL                                      |
| **content**         | TEXT        | Message text         | NOT NULL                                      |
| **progress\_score** | INTEGER     | Evaluator score      | NULLABLE                                      |
| **created\_at**     | TIMESTAMP   | Creation time        | NOT NULL, DEFAULT NOW()                       |

-----

## Section 3 — Pydantic Models

``` python
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

# 1. POST /v1/session
class SessionRequest(BaseModel):
    content: str  # Problem text

class SessionResponse(BaseModel):
    session_id: UUID
    role: str            # "coach"
    content: str         # The opening Socratic question
    hint_level: int      # Typically starting at 1
    session_status: str  # e.g., "active"

# 2. POST /v1/session/{id}/message
class MessageRequest(BaseModel):
    content: str  # User response text

class MessageResponse(BaseModel):
    role: str  # "coach"
    content: str  # Socra's next question
    hint_level: int
    session_status: str

# 3. GET /v1/session/{id}
class MessageModel(BaseModel):
    role: str  # "student" or "coach"
    content: str
    created_at: datetime

class SessionHistoryResponse(BaseModel):
    session_id: UUID
    problem_text: str
    status: str
    messages_list: list[MessageModel]

```

-----

## Section 4 — Strategy Engine Logic

``` python
def run_strategy_engine(session_context, latest_progress_score):
    # 1. Read existing state variables
    current_stage = session_context.current_stage
    current_hint_level = session_context.current_hint_level
    consecutive_stuck_count = session_context.stuck_count
    
    # 2. Evaluate State Transitions
    if latest_progress_score >= STAGE_COMPLETE_SCORE:
        current_stage = advance_to_next_cognitive_stage(current_stage)
        consecutive_stuck_count = 0
        current_hint_level = 0
        response_type = "GUIDING_QUESTION"
    elif latest_progress_score > 0:
        consecutive_stuck_count = 0
        response_type = "GUIDING_QUESTION"
    else:
        consecutive_stuck_count += 1
        
        if consecutive_stuck_count >= MAX_STUCK_THRESHOLD:
            if current_hint_level < 5:
                current_hint_level += 1
            consecutive_stuck_count = 0
            response_type = "HINT"
        else:
            response_type = "CLARIFYING_PROBE"

    # 3. Resolve prompt instruction
    llm_instruction = generate_prompt_boundary_rules(current_stage, response_type, current_hint_level)
    
    # 4. Save metrics
    updated_state = {
        "next_stage": current_stage,
        "next_hint_level": current_hint_level,
        "updated_stuck_count": consecutive_stuck_count
    }
    
    return package_structured_llm_request(llm_instruction, updated_state, session_context.history)

def generate_prompt_boundary_rules(stage, response_type, hint_level):
    base_rule = "STRICT: Do not provide code blocks. Do not state the final algorithm directly."
    
    if response_type == "GUIDING_QUESTION":
        return base_rule + f" Analyze history for stage {stage}. Ask exactly one forward-moving conceptual question."
    if response_type == "CLARIFYING_PROBE":
        return base_rule + " The student is circling. Ask them to isolate inputs/outputs or restate their assumption."
    if response_type == "HINT":
        if hint_level == 1:
            return base_rule + " Action: Ask a reflective question tracking what they have tried so far step-by-step."
        elif hint_level == 2:
            return base_rule + " Action: Point out a structural observation regarding input constraints or bounds."
        elif hint_level == 3:
            return base_rule + " Action: Deliver a directional nudge orienting them toward output traits."
        elif hint_level == 4:
            return base_rule + " Action: Ask a near-explicit question naming optimal complexities."
        elif hint_level == 5:
            return "EXUANCE RULE: All hints exhausted. Provide a clear text explanation of the algorithm approach. Still do not write raw code."

```

-----

## Section 5 — Progress Evaluator

``` python
def evaluate_student_progress(student_message, active_stage, problem_metadata):
    # Normalize message strings
    normalized_msg = student_message.lower()
    
    # Rule 1: Capitulation (Score 0)
    stuck_keywords = ["i don't know", "i'm stuck", "no idea", "help me", "clueless", "confused"]
    for keyword in stuck_keywords:
        if keyword in normalized_msg:
            return 0
            
    # Rule 2: Breakthrough Conditions (Score 3)
    if active_stage == "UC1" and student_has_isolated_io_bounds(normalized_msg, problem_metadata):
        return 3
    elif active_stage == "UC2" and student_has_derived_brute_force(normalized_msg, problem_metadata):
        return 3
    elif active_stage == "UC3" and student_has_isolated_bottleneck(normalized_msg, problem_metadata):
        return 3
    elif active_stage == "UC4" and student_has_named_correct_dsa_pattern(normalized_msg, problem_metadata):
        return 3
    elif active_stage == "UC5" and student_has_mapped_optimal_implementation(normalized_msg, problem_metadata):
        return 3
        
    # Rule 3: Conceptual Progress (Score 2)
    progress_keywords = problem_metadata.optimal_pattern_keywords
    for keyword in progress_keywords:
        if keyword in normalized_msg:
            return 2
            
    # Rule 4: Structural Exploration (Score 1)
    exploration_keywords = ["constraint", "size", "array length", "index", "what if", "negative"]
    for keyword in exploration_keywords:
        if keyword in normalized_msg:
            return 1
            
    return 0

```
