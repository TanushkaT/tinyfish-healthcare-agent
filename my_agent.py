import json
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Setup Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("⚠️ Warning: GEMINI_API_KEY not found in .env")

# 3. Setup TinyFish API Key
TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY")

if not TINYFISH_API_KEY:
    print("❌ Error: TINYFISH_API_KEY not found! Please add it to your .env file.")
    exit()

def run_web_agent(target_url, goal_description):
    print(f"\n🚀 Starting Agent on: {target_url}")
    print(f"🎯 Goal: {goal_description}\n")
    
    api_url = "https://agent.tinyfish.ai/v1/automation/run-sse"
    
    headers = {
        "X-API-Key": TINYFISH_API_KEY,
        "Content-Type": "application/json",
    }
    
    payload = {
        "url": target_url,
        "goal": goal_description,
    }

    try:
        # We use the 'with' block to keep the connection open for the stream
        with requests.post(api_url, headers=headers, json=payload, stream=True) as response:
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return
            
            # THE LOOP MUST BE INSIDE THE 'WITH' BLOCK
            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8").strip()
                    if line_str.startswith("data: "):
                        try:
                            event = json.loads(line_str[6:])
                            event_type = event.get("type")
                            
                            if event_type == "HEARTBEAT":
                                print("💓 Agent is navigating and thinking...")
                            
                            elif event_type in ["AGENT_RESULT", "COMPLETE", "FINISH"]:
                                print("\n" + "="*40)
                                print("✅ SUCCESS: DATA EXTRACTED")
                                print("="*40)
                                # Show the actual final data
                                print(json.dumps(event.get("data"), indent=4))
                                print("="*40 + "\n")
                                break 
                            
                            else:
                                print(f"📡 {event_type}: {event.get('message', 'Processing...')}")
                                
                        except json.JSONDecodeError:
                            continue
                        
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    run_web_agent(
        target_url="https://agentql.com", 
        goal_description="Find all subscription plans and their prices. Return the result in a clean JSON format."
    )
