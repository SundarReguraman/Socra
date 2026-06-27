# Socra

An AI-powered Socratic reasoning coach that helps students develop problem-solving intuition for Data Structures and Algorithms (DSA) problems.

## What is Socra?

Socra guides students through complex DSA problems using adaptive questioning and a structured hint system—teaching them *how to think*, not *what to think*. Instead of handing out solutions, it evaluates user responses dynamically to offer contextual nudges or structural hints.

---

## 🚀 Status: Active Development

We have officially transitioned from the documentation phase to active engineering.

- [x] Press Release (PR)
- [x] Product Requirements Document (PRD)
- [x] High-Level Design (HLD)
- [x] Low-Level Design (LLD)
- [ ] Backend Implementation (FastAPI + Supabase)
- [ ] Frontend Implementation (React + Vercel)

---

## 🛠️ Tech Stack

* **Frontend:** React, Tailwind CSS (Hosted on Vercel)
* **Backend:** FastAPI, Python (Hosted on Railway)
* **Database:** PostgreSQL, Supabase
* **LLM Engine:** Anthropic Claude (via API wrapper)

---

## 📂 Documentation & Blueprints

All system specifications, foundational narratives, and architectural designs are located under the `docs/` directory:
* [Press Release](docs/press_release.md) — Future-dated launch announcement highlighting the core vision and student impact.
* [Product Requirements Document](docs/prd.md) — Core features, user personas, and product scope.
* [High-Level Design](docs/hld.md) — System architecture, sequence diagrams, and block components.
* [Low-Level Design](docs/lld.md) — Exact API contracts, Pydantic data validation schemas, database layout, and state machine algorithms.

---

## 💻 Local Development Setup

### Backend (FastAPI)
1. Navigate to the backend folder:
   ```bash
   cd backend
Here is the content converted into a clean Markdown format for your documentation:

```` markdown
### Backend (Python)

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

````

2.  **Install dependencies:**
    
    ``` bash
    pip install -r requirements.txt
    
    ```

3.  **Run the development server:**
    
    ``` bash
    python manage.py runserver
    
    ```

### Frontend (React)

1.  **Navigate to the frontend folder:**
    
    ``` bash
    cd frontend
    
    ```

2.  **Install the node packages:**
    
    ``` bash
    npm install
    
    ```

3.  **Start the local server:**
    
    ``` bash
    npm start
    
    ```

<!-- end list -->

``` 
 
```
