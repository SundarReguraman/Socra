# Socra

An AI-powered Socratic reasoning coach that helps students develop problem-solving intuition for Data Structures and Algorithms (DSA) problems.

## What is Socra?

Socra guides students through complex DSA problems using adaptive questioning and a structured hint system—teaching them *how to think*, not *what to think*. Instead of handing out solutions, it utilizes a **closed-loop state machine** to evaluate user responses dynamically, offering contextual nudges that advance students through logical problem-solving stages.

---

## 🚀 Status: Active Development

We have officially transitioned from the documentation phase to active engineering.

- [x] Press Release (PR)
- [x] Product Requirements Document (PRD)
- [x] High-Level Design (HLD)
- [x] Low-Level Design (LLD)
- [x] Backend API & Database Implementation (FastAPI + Supabase)
- [x] Prompt Engineering & State Management 
- [x] Frontend UI Integration (React + Vercel)

---

## 🛠️ Tech Stack

<div align="left">

**Frontend:** React & Tailwind CSS (Hosted on Vercel) <br>
<img src="https://skillicons.dev/icons?i=react,tailwind&theme=dark" alt="React and Tailwind" />
<br><br>

**Backend:** Python & FastAPI (Hosted on Railway) <br>
<img src="https://skillicons.dev/icons?i=python,fastapi&theme=dark" alt="Python and FastAPI" />
<br><br>

**Database:** PostgreSQL & Supabase <br>
<img src="https://skillicons.dev/icons?i=postgres,supabase&theme=dark" alt="PostgreSQL and Supabase" />
<br><br>

**LLM Engine:** Google Gemini API (`gemini-2.5-flash`) <br>
<img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/google-gemini-icon.svg" width="48" height="48" alt="Google Gemini" />

</div>


## 📂 Documentation & Blueprints

All system specifications, foundational narratives, and architectural designs are located under the `docs/` directory:
* [Press Release](docs/press_release.md) — Future-dated launch announcement highlighting the core vision and student impact.
* [Product Requirements Document](docs/prd.md) — Core features, user personas, and product scope.
* [High-Level Design](docs/hld.md) — System architecture, sequence diagrams, and block components.
* [Low-Level Design](docs/lld.md) — Exact API contracts, Pydantic data validation schemas, database layout, and state machine algorithms.
* [Entity Relationship Diagram](docs/erd.md) — Database layout schemas, data types, and primary/foreign key connections.
* [API Contracts](docs/api_contracts.md) — Structural endpoint constraints, payloads, and response expectations.

---

## 💻 Local Development Setup

### Backend (FastAPI)

1. **Navigate to the backend folder:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root of the `backend/` directory and add your secure keys:
   ```env
   DATABASE_URL="your_supabase_postgres_connection_string"
   GEMINI_API_KEY="your_google_ai_studio_key"
   ```

5. **Run the development server:**
   ```bash
   uvicorn main:app --reload
   ```
   *The server will start at `http://localhost:8000`.*

---

### Frontend (React)

1. **Navigate to the frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install the node packages:**
   ```bash
   npm install
   ```

3. **Start the local server:**
   ```bash
   npm start
   ```
   *Ensure your local API fetch URL is pointing to `http://localhost:8000` to interact with the local backend!*
