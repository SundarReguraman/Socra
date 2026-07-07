from llm_gateway import get_llm_response

def evaluate_progress(problem_text: str, messages: list, student_response:str) -> int:
    conversation_history = ""
    for message in messages:
        role = "Student" if message.sender == "student" else "Socra"
        conversation_history += f"{role}: {message.content}\n"

    prompt = f"""
You are evaluating a student's progress toward solving a DSA problem.

PROBLEM:
{problem_text}

CONVERSATION SO FAR:
{conversation_history}

STUDENT'S LATEST RESPONSE:
{student_response}

Score the student's latest response based on how much progress they are making toward the optimal solution.

Return ONLY a single integer score — nothing else. No explanation. No preamble.

Scoring rules:
0 — Student is repeating themselves, going in circles, or showing no new understanding
1 — Student is asking a clarifying question or showing partial understanding
2 — Student mentions a relevant concept, pattern, or data structure
3 — Student has identified the key insight or optimal approach

Return only the integer: 0, 1, 2, or 3
"""
    response = get_llm_response(prompt)

    try:
        score = int(response.strip())
        if score not in [0,1,2,3]:
            return 1
        return score
    except:
        return 1
    