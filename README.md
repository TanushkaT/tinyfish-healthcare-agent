# tinyfish-healthcare-agent

## 🏥 Healthcare Appointment Orchestration Agent
Built with TinyFish Web Agent API

### ⚠️ The Problem
Healthcare coordinators currently waste hours manually logging into fragmented hospital portals. These systems are dynamic, session-based, and lack unified APIs. This leads to:
Slow Coordination: Checking multiple specialists one-by-one.
Human Error: Repeatedly re-entering patient data manually.
Scalability Issues: Costs rise as appointment volumes increase.

### ✅ The Solution
An autonomous agent acts as an AI scheduling operator. It uses the TinyFish API to:
Navigate complex, JS-heavy hospital booking systems.
Authenticate and maintain secure sessions.
Extract real-time availability and auto-fill patient forms.
Confirm bookings end-to-end without human intervention.

### 🛠️ Tech Stack
The autonomous agent is built using a modern, scalable stack designed for high-performance web automation:
Core Infrastructure: TinyFish Web Agent API — Handles authenticated browser sessions and dynamic navigation.
Language: Python 3.10+ — Used for backend logic and API orchestration.
AI Engine: Google Gemini (1.5 Flash) — Acts as the "brain" to process unstructured web data and understand complex UI elements.
Networking: requests & google-generativeai — For high-speed communication and LLM integration.
Data Handling: JSON & Pydantic — Ensures all extracted data is structured and validated.

### 💡 Why this stack?
By combining TinyFish with Google Gemini, the agent moves beyond simple "web scraping." The agent uses Gemini's advanced reasoning to navigate hospital workflows and perform real transactions without needing a formal API, all while remaining cost-effective and developer-friendly.

### Setup Instructions:
pip install requests python-dotenv google-generativeai
Add your TINYFISH_API_KEY and GEMINI_API_KEY to a .env file.
python my_agent.py
