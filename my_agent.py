import json
import os
import requests
from dotenv import load_dotenv

# This loads the variables from the .env file
load_dotenv()

# Now you can access them safely
TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
        stream=True, # Allows us to see the agent's progress live
    )

    for line in response.iter_lines():
        if line:
            line_str = line.decode("utf-8")
            if line_str.startswith("data: "):
                # Parse the progress or final result
                event = json.loads(line_str[6:])
                print(f"🤖 Agent Status: {event}")

# 2. Test Goal: Extract details from a sample site
run_web_agent(
    "https://agentql.com", 
    "Find all subscription plans and their prices. Return result in json format"
)
