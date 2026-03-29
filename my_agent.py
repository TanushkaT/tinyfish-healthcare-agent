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
    """
    Connects to TinyFish API, navigates the web, and streams results live.
    Includes a timeout fix for GitHub Codespaces stability.
    """
    print(f"\n🚀 Starting Agent on: {target_url}")
    print(f"🎯 Goal: {goal_description}\n")
    
    # Official TinyFish SSE endpoint
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
        # 'stream=True' and 'timeout' keep the cloud connection from closing early
        with requests.post(api_url, headers=headers, json=payload, stream=True, timeout=300) as response:
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return
            
            # Iterate through the Server-Sent Events (SSE)
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    line_str = line.strip()
                    if line_str.startswith("data: "):
                        try:
                            event = json.loads(line_str[6:])
                            event_type = event.get("type")
                            
                            # SHOW THIS IN YOUR VIDEO: Proves the agent is active
                            if event_type == "HEARTBEAT":
                                print("💓 Agent is navigating and thinking...")
                            
                            # CATCH ANY DATA RECEIVED
                            data = event.get("data")
                            if data is not None:
                                print("\n" + "="*40)
                                print(f"✅ DATA RECEIVED ({event_type})")
                                print("="*40)
                                print(json.dumps(data, indent=4))
                                print("="*40 + "\n")
                                
                                # If it's a final event, we can safely stop
                                if event_type in ["AGENT_RESULT", "COMPLETE", "FINISH"]:
                                    break 
                            
                            # Show status messages so the video looks active
                            elif event.get("message"):
                                print(f"📡 Status: {event.get('message')}")
                                
                        except json.JSONDecodeError:
                            continue
                        
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    # We use Google for the demo because it's fast and reliable
    run_web_agent(
        target_url="https://www.google.com", 
        goal_description="Extract the text of the 'About' and 'Advertising' links at the bottom of the page. Return as a JSON list."
    )
