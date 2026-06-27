# API Contracts — Socra v1

## Global Configuration

**Base URL:** <https://api.socra.com>  
**Authentication:** All endpoints require a valid JWT token in the request header.

``` json
Authorization: Bearer <token>
Content-Type: application/json

```

-----

## Endpoint 1: Create a Session

**Route:** `POST /v1/session`  
**Description:** Initializes a new coaching session when a student submits a problem.

**Request body:**

``` json
{
  "problem_text": "Given an array of integers nums..."
}

```

**Success Response (201 Created):**

``` json
{
  "session_id": "abc123",
  "role": "coach",
  "content": "The problem mentions that...",
  "hint_level": 0,
  "session_status": "active"
}

```

**Errors:**
| Code | Reason |
| :--- | :--- |
| 400 | Empty or missing problem\_text in request body |
| 401 | Missing or invalid JWT token |
| 503 | Server unavailable due to excessive load |

-----

## Endpoint 2: Send a Message

**Route:** `POST /v1/session/{id}/message`  
**Description:** Submits student input and retrieves the AI coach's next response or hint.

**Request body:**

``` json
{
  "content": "How do I initialize the value of mid"
}

```

**Success Response (200 OK):**

``` json
{
  "role": "coach",
  "content": "You have your left and right pointers at both ends...",
  "hint_level": 2,
  "session_status": "active"
}

```

**Errors:**
| Code | Reason |
| :--- | :--- |
| 401 | Missing or invalid JWT token |
| 404 | Session ID not found in the URL path |
| 422 | Request body missing the content field |

-----

## Endpoint 3: Retrieve Session History

**Route:** `GET /v1/session/{id}`  
**Description:** Fetches the complete conversation thread for a specific session.  
**Request Body:** *None*

**Success Response (200 OK):**

``` json
{
  "session_id": "abc123",
  "messages": [
    { "role": "student", "content": "I'm stuck..." },
    { "role": "coach", "content": "What happens when..." }
  ]
}

```

**Errors:**
| Code | Reason |
| :--- | :--- |
| 401 | Missing or invalid JWT token |
| 404 | Session ID does not exist |
| 500 | Retrieved data fails Pydantic schema validation |

-----

