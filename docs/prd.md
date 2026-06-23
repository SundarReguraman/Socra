# Product Requirements Document (PRD) — Socra v1

## Problem Statement
Students learn Data Structures and Algorithms (DSA) concepts thoroughly, but when it comes to actually solving an unseen problem and figuring out the most optimal approach, they struggle. After trying for a while and being unable to come up with an approach, they resort to watching tutorials or asking standard AIs to hand them the logic.

This loop inhibits students from independently deriving solutions — which is the exact process through which logical thinking is developed. This skill is non-negotiable for landing roles at FAANG and top-tier big tech companies.

---

## Target User Persona
* **Name:** Aditya, 3rd-year CSE student
* **Goal:** Preparing for campus placements for roles at Big Tech companies.
* **Context:** He has prepared DSA for months and understands core concepts like Arrays, Graphs, and Trees. When he watches tutorials and reads editorials, they make complete sense.
* **The Pain Point:** When facing an unseen Leetcode Medium problem (e.g., on Graphs), his thinking stalls. Sometimes he can piece together a brute-force approach, but he struggles to optimize it or find the key insight that reduces time complexity. After 30–45 minutes of going in circles, he gives up and looks up the solution.

> **The Core Intercept:** Socra is built precisely for this moment — not before he attempts the problem, and not after he has given up. It intercepts when he is genuinely stuck and willing to think, but needs direction.

---

## Use Cases

### 1. Cannot Understand the Problem
* **Situation:** User understands BFS as a concept and opens an unseen medium-level Leetcode problem.
* **Failure Point:** They cannot process what the problem is actually asking, leading them to read it multiple times without translating it into actionable steps.
* **Need:** Socra guides them to read the problem structurally — identifying inputs, outputs, and constraints — before any solution thinking begins.

### 2. Cannot Come Up with a Brute Force Approach
* **Situation:** The user understands the DSA concepts and can break down the inputs, outputs, and requirements.
* **Failure Point:** They cannot come up with a baseline brute force approach — even a naive, inefficient solution is out of reach. They don't know where to begin.
* **Need:** Socra asks questions that take specific aspects of the problem the user already understands and connects them toward a starting point without revealing the solution.

### 3. Unable to Identify Complexity Bottlenecks
* **Situation:** The user successfully comes up with a brute force solution.
* **Failure Point:** They are unable to analyze and find the Time and Space complexity bottlenecks of their brute force approach to see why it will fail the constraints.
* **Need:** Socra takes the problem and their brute force approach and asks questions that push the user to identify bottlenecks based upon input size and edge cases.

### 4. Unaware of the Concept Needed for Optimization
* **Situation:** The user has moved from understanding the problem to identifying why their brute-force solution fails.
* **Failure Point:** They cannot bridge the gap to identify *which* specific DSA concept works best to resolve the bottleneck.
* **Need:** Socra asks the user what they want to achieve structurally (e.g., storing indices, frequency maps, fast lookups, or specific traversals) to guide them to the right concept.

### 5. Concept Application Mismatch
* **Situation:** The user knows exactly which DSA concept needs to be applied to arrive at the optimal approach.
* **Failure Point:** They are unable to figure out *how* to apply that concept specifically to obtain the optimal solution architecture.
* **Need:** Socra asks the user how they want their solution logic to flow in line with the required concept while satisfying constraints.

---

## Product Scope

### In-Scope (v1)
1. **Problem Ingestion:** Users paste the Leetcode problem along with input constraints and example cases. Socra parses this to use as the baseline foundation for the session.
2. **Session Management:** Keeps track of the chat history within a single session to monitor progress and ensure the user is not moving in circles.
3. **Adaptive Questioning:** The brain of Socra. It evaluates successive user responses, maps their forward progress or deviations relative to the optimal solution, and asks tailored guiding questions.
4. **Hint System:** An escalating 5-level hint workflow triggered if a user remains stuck:
   * *Level 1:* Reflective Hint
   * *Level 2:* Observational Hint
   * *Level 3:* Directional Nudge
   * *Level 4:* Partially Explicit Hint
   * *Level 5:* Fully Explicit Hint (reveals the approach logic)
5. **Progress Tracking:** Monitors the momentum from the first exchange to the last, feeding data back into the adaptive questioning engine to trigger hints if stagnation is detected.
6. **Session Conclusion:** Handles clean termination states — celebrating when a user reaches the optimal approach or managing fallback mechanisms when explicit hints become a necessity.

### Out of Scope (v1)
* **Cross-session memory & analytics:** Remembering solved problems or tracking multi-session metrics.
* **Pattern recognition & logic tracking:** Surfacing cross-problem structural similarities or maintaining student knowledge graphs.
* **Inbuilt IDE & Debugging:** Code execution blocks or debugger helpers; users write code in their own external IDE and paste logic blocks into Socra if needed.
* **Screen Context & Extensions:** Chrome extensions or side-panels that actively scrape browser screens.
* **Platform APIs:** Direct API integrations with Leetcode/Codeforces; copy-paste is sufficient for v1.

---

## Success Metrics
* **Session Length:** Target of ~10 exchanges per session. (Too high implies inefficient hints; too low implies giving up early or trivial problem choices).
* **Session Completion Rate:** Target $\ge$ 70% of sessions successfully ending with the user arriving at the optimal approach independently without being handed the solution outright.
* **Hint Escalation Rate:** Fewer than 2 escalations to Level 5 (Fully Explicit) per session.
* **D7 Retention:** Target of 40% of signed-up users returning within 7 days.
* **Time to Second Session:** Target within 24 to 48 hours of completing the first problem.

---

## What "Done" Looks Like (End-to-End User Flow)
Aditya opens Socra and pastes in the *Jump Game* problem — a medium-level Leetcode problem he has been staring at for 40 minutes. 

1. Socra reads the problem text and asks: *"What does the value at each index actually represent, and what are you trying to find out by the end?"*
2. Aditya answers. Socra evaluates his response, determines he understands the problem foundations, and follows up: *"You mentioned you can jump up to that many steps. From index 0 with a value of 2, which indices can you actually reach?"*
3. Aditya maps it out. Socra monitors his correct baseline path and guides him toward the optimization step: *"You have a brute force in mind. What is the worst-case scenario of your current approach and why does it fail?"*
4. Aditya explicitly states the runtime bottlenecks. 
5. Socra detects forward momentum and asks the critical design prompt: *"Given that you're recomputing reachability at every step, what single value, if you tracked it, would tell you whether the last index is reachable?"*
6. Aditya pauses, considers it, and types: *"The maximum index I can reach from any position I've visited so far."*
7. Socra confirms he has broken through the bottleneck and bridges him to code implementation: *"If that maximum reachable index ever falls behind your current position, what does that tell you?"*
8. Aditya replies: *"That I'm stuck. I can't move forward."*

He immediately minimizes the screen, opens his IDE, and writes the code himself. **Ten exchanges. Zero explicit hints.** The approach was already inside him; Socra just helped him find it.
