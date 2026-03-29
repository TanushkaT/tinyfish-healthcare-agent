import json
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY")

def run_web_agent(target_url, goal_description):
    print(f"🚀 Starting Agent on: {target_url}")
    api_url = "https://agent.tinyfish.ai/v1/automation/run-sse"
    
    headers = {
        "X-API-Key": TINYFISH_API_KEY,
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    payload = {"url": target_url, "goal": goal_description}

    # Setting a longer timeout (5 minutes) specifically for Codespaces
    try:
        with requests.post(api_url, headers=headers, json=payload, stream=True, timeout=300) as response:
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code}")
                return

            # This line-by-line reading is the most stable for SSE streams
            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    event = json.loads(line[6:])
                    event_type = event.get("type")
                    
                    if event_type == "HEARTBEAT":
                        print("💓 Agent is working (Stay alive)...")
                    
                    # We print ANY non-empty data immediately
                    data = event.get("data")
                    if data:
                        print("\n" + "="*40 + "\n✅ SUCCESS: DATA RECEIVED!\n" + "="*40)
                        print(json.dumps(data, indent=4))
                        print("="*40 + "\n")
                        return # This stops the script ONLY after printing the data
                        
                    elif event.get("message"):
                        print(f"📡 Status: {event.get('message')}")

    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    # Using Google for the demo because it is fast and reliable
    run_web_agent(
        "https://www.google.com", 
        "Find the 'About' link at the bottom and return its text as a JSON list."
    )
