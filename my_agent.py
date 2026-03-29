import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY")

def run_web_agent(target_url, goal_description):
    print(f"🚀 Starting Agent on: {target_url}")
    # CORRECT ENDPOINT URL
    api_url = "https://agent.tinyfish.ai/v1/automation/run-sse"
    
    headers = {"X-API-Key": TINYFISH_API_KEY, "Content-Type": "application/json"}
    payload = {"url": target_url, "goal": goal_description}

    # 'stream=True' and a long timeout prevent Codespaces from killing the process
    with requests.post(api_url, headers=headers, json=payload, stream=True, timeout=120) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data: "):
                event = json.loads(line[6:])
                event_type = event.get("type")
                
                if event_type == "HEARTBEAT":
                    print("💓 Agent is still thinking... (Stay alive)")
                
                # Check for ANY data or message
                data = event.get("data")
                if data:
                    print("\n" + "="*40 + "\n✅ SUCCESS: DATA RECEIVED!\n" + "="*40)
                    print(json.dumps(data, indent=4))
                    print("="*40 + "\n")
                    return # Exit ONLY after printing data
                
                elif event.get("message"):
                    print(f"📡 Status: {event.get('message')}")

if __name__ == "__main__":
    run_web_agent(
        "https://www.google.com", 
        "Find the 'About' link at the bottom and return its text as a JSON list."
    )
