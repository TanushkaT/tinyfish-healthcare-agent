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
    
    with requests.post(
        "https://agent.tinyfish.ai",
        headers={"X-API-Key": TINYFISH_API_KEY, "Content-Type": "application/json"},
        json={"url": target_url, "goal": goal_description},
        stream=True,
    ) as response:
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8").strip()
                if line_str.startswith("data: "):
                    try:
                        event = json.loads(line_str[6:])
                        
                        if event.get("type") == "HEARTBEAT":
                            print("💓 Agent is navigating and thinking...")
                        
                        # Use this to catch the final result specifically
                        elif event.get("type") in ["AGENT_RESULT", "FINISH", "DONE"]:
                            print("\n" + "="*30 + "\n✅ SUCCESS!\n" + "="*30)
                            print(json.dumps(event.get("data"), indent=4))
                            break # Exit the loop once we have the result
                            
                        # Catch any other updates so the terminal isn't empty
                        else:
                            print(f"📡 Status: {event.get('type')}")
                            
                    except json.JSONDecodeError:
                        continue

    # THIS WAS MOVED RIGHT BY 4 SPACES
    for line in response.iter_lines():
        if line:
            line_str = line.decode("utf-8")
            if line_str.startswith("data: "):
                event = json.loads(line_str[6:])
                
                # 1. Always show the heartbeat so you know it's working
                if event.get("type") == "HEARTBEAT":
                    print("💓 Agent is navigating and thinking...")
                
                # 2. Print ANY data the agent sends back
                # This catches 'AGENT_RESULT', 'ACTION_COMPLETED', and others
                elif "data" in event:
                    print("\n" + "="*30)
                    print(f"📡 AGENT UPDATE: {event.get('type')}")
                    print("="*30)
                    print(json.dumps(event.get("data"), indent=4))
                    print("="*30 + "\n")
                    
# 2. Test Goal: Extract details from a sample site
run_web_agent(
    "https://agentql.com", 
    "Find all subscription plans and their prices. Return result in json format"
)
