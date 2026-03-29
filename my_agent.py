import json
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# This loads the variables from the .env file
load_dotenv()

# Setup Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def process_with_gemini(web_data):
    prompt = f"You are a healthcare assistant. Based on this website data: {web_data}, find the best appointment slot and return only the date and time."
    
    response = model.generate_content(prompt)
    return response.text

# Now you can access them safely
TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY")

# Test it
if not TINYFISH_API_KEY:
    print("❌ Error: API Key not found!")


def run_web_agent(target_url, goal_description):
    print(f"🚀 Starting agent on: {target_url}...")
    
    response = requests.post(
        "https://agent.tinyfish.ai/v1/automation/run-sse",
        headers={
            "X-API-Key": TINYFISH_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "url": target_url,
            "goal": goal_description,
        },
        stream=True, 
    )

    # THIS WAS MOVED RIGHT BY 4 SPACES
    for line in response.iter_lines():
        if line:
            line_str = line.decode("utf-8")
            if line_str.startswith("data: "):
                event = json.loads(line_str[6:])
                
                if event.get("type") == "HEARTBEAT":
                    print("💓 Agent is thinking...")
                
                elif event.get("type") == "AGENT_RESULT":
                    print("\n" + "="*30)
                    print("✅ TASK COMPLETED SUCCESSFULLY")
                    print("="*30)
                    print(json.dumps(event.get("data"), indent=4))
                    print("="*30 + "\n")

# 2. Test Goal: Extract details from a sample site
run_web_agent(
    "https://agentql.com", 
    "Find all subscription plans and their prices. Return result in json format"
)
