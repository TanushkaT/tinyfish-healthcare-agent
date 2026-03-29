import json
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load environment variables from your .env file
load_dotenv()

# 2. Setup Google Gemini (Free AI Brain)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("⚠️ Warning: GEMINI_API_KEY not found in .env")

# 3. Setup TinyFish API Key
TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY")

if not TINYFISH_API_KEY:
    print("❌ Error: TINYFISH_API_KEY not found in .env! Please add it.")
    exit()

def run_web_agent(target_url, goal_description):
    """
    Connects to TinyFish API, navigates the web, and streams results live.
    """
    print(f"\n🚀 Starting Agent on: {target_url}")
    print(f"🎯 Goal: {goal_description}\n")
    
    # TinyFish SSE endpoint for live automation
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
        # Use 'with' to keep the connection open during the stream
        with requests.post(api_url, headers=headers, json=payload, stream=True) as response:
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return

            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8").strip()
                    
                    # Parse Server-Sent Events (SSE) starting with 'data: '
                    if line_str.startswith("data: "):
                        try:
                            event = json.loads(line_str[6:])
                            event_type = event.get("type")
                            
                            # SHOW THIS IN YOUR VIDEO: The "Heartbeat" proves the agent is active
                            if event_type == "HEARTBEAT":
                                print("💓 Agent is navigating and thinking...")
                            
                            # SHOW THIS IN YOUR VIDEO: The Final Result
                            elif event_type in ["AGENT_RESULT", "FINISH", "DONE"]:
                                print("\n" + "="*40)
                                print("✅ TASK COMPLETED SUCCESSFULLY")
                                print("="*40)
                                print(json.dumps(event.get("data"), indent=4))
                                print("="*40 + "\n")
                                break # Stop once we have the result
                            
                            # Show other status updates so the terminal isn't silent
                            else:
                                print(f"📡 Status Update: {event_type}")
                                
                        except json.JSONDecodeError:
                            continue

    except Exception as e:
        print(f"❌ An error occurred: {e}")

# 4. EXECUTION (The demo goal)
if __name__ == "__main__":
    # Test on a reliable site for your demo video
    run_web_agent(
        target_url="https://agentql.com", 
        goal_description="Find all subscription plans and their prices. Return the result in a clean JSON format."
    )
