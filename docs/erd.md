# Entity Relationship Diagram (ERD)

Below is the database schema represented as an Entity Relationship Diagram:

```mermaid
erDiagram
  USERS ||--o{ SESSIONS : has
  SESSIONS ||--o{ MESSAGES : contains

  USERS {
    UUID id PK
    VARCHAR name
    VARCHAR email
    TIMESTAMP signup_time
    VARCHAR auth_provider
  }

  SESSIONS {
    UUID id PK
    UUID user_id FK
    TEXT problem_text
    INTEGER current_hint_level
    VARCHAR status
    TIMESTAMP created_at
  }

  MESSAGES {
    UUID id PK
    UUID session_id FK
    VARCHAR sender
    TEXT content
    INTEGER progress_score
    TIMESTAMP created_at
  }
