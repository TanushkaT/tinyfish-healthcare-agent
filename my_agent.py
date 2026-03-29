import json
import os
import requests

# 1. Replace with your actual API key
TINYFISH_API_KEY = "YOUR_API_KEY_HERE"

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
