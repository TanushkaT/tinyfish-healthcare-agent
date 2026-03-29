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

    # 'with' keeps the connection open
    with requests.post(api_url, headers=headers, json=payload, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data: "):
                event = json.loads(line[6:])
                
                if event.get("type") == "HEARTBEAT":
                    print("💓 Agent is thinking...")
                
                # Check for any message or data chunk
                elif event.get("data"):
                    print("\n" + "="*40 + "\n✅ DATA RECEIVED!\n" + "="*40)
                    print(json.dumps(event.get("data"), indent=4))
                    print("="*40 + "\n")
                    break # Only stop AFTER printing data
                
                elif event.get("message"):
                    print(f"📡 Status: {event.get('message')}")

if __name__ == "__main__":
    run_web_agent(
        "https://www.google.com", 
        "Extract the text of the 'About' and 'Advertising' links at the bottom of the page. Return as a JSON list."
    )
