import json
import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
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

    # Using a Session keeps the 'handshake' alive longer in Codespaces
    session = requests.Session()
    
    try:
        with session.post(api_url, headers=headers, json=payload, stream=True, timeout=300) as response:
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code}")
                return

            # Read line by line until the agent is DONE
            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    try:
                        event = json.loads(line[6:])
                        event_type = event.get("type")
                        
                        if event_type == "HEARTBEAT":
                            print("💓 Agent is still thinking... (Stay alive)")
                        
                        # Catch ANY data chunk
                        data = event.get("data")
                        if data:
                            print("\n" + "="*40 + "\n✅ SUCCESS: DATA RECEIVED!\n" + "="*40)
                            print(json.dumps(data, indent=4))
                            print("="*40 + "\n")
                            return # EXIT ONLY AFTER PRINTING DATA
                            
                        elif event.get("message"):
                            print(f"📡 Status: {event.get('message')}")
                            
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_web_agent(
        "https://www.google.com", 
        "Find the 'About' link at the bottom and return its text as a JSON list."
    )
