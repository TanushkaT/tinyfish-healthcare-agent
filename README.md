# tinyfish-healthcare-agent
Project Title:
## 🏥 Healthcare Appointment Orchestration Agent
**Built with TinyFish Web Agent API**

### ⚠️ The Problem
Healthcare coordinators currently waste hours manually logging into fragmented hospital portals. These systems are dynamic, session-based, and lack unified APIs. This leads to:
* **Slow Coordination:** Checking multiple specialists one-by-one.
* **Human Error:** Repeatedly re-entering patient data manually.
* **Scalability Issues:** Costs rise as appointment volumes increase.

### ✅ The Solution
Our autonomous agent acts as an AI scheduling operator. It uses the **TinyFish API** to:
1. **Navigate** complex, JS-heavy hospital booking systems.
2. **Authenticate** and maintain secure sessions.
3. **Extract** real-time availability and auto-fill patient forms.
4. **Confirm** bookings end-to-end without human intervention.

# 🛠️ Tech Stack:
Our autonomous agent is built using a modern, scalable stack designed for high-performance web automation and intelligent decision-making:
Core Infrastructure: TinyFish Web Agent API — Handles authenticated browser sessions, dynamic JavaScript rendering, and multi-step navigation.
Language: Python 3.10+ — Used for backend logic and API orchestration.
AI Engine: OpenAI (GPT-4o) — Acts as the "brain" to process unstructured web data, understand complex UI elements, and rank appointment slots based on user intent.
Networking: requests & AIOHTTP — For high-speed, asynchronous communication with the TinyFish automation nodes.
Data Handling: JSON & Pydantic — Ensures all extracted data from hospital portals is structured and validated for the booking process.
# 💡 Why this stack?
By combining TinyFish with OpenAI, we move beyond simple "web scraping." Our agent doesn't just read data; it reasons through different hospital workflows and performs real transactions without needing a formal API from the hospitals.

# Setup Instructions:
1. pip install requests
2. python my_agent.py
