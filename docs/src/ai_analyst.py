import json
import time
import requests
import os

# Configuration
LOG_FILE = "/var/ossec/logs/alerts/alerts.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"
TARGET_RULE = "100001"

def tail_file(file_path):
    """Reads the file and follows for new lines."""
    with open(file_path, "r") as f:
        # REMOVED: f.seek(0, os.SEEK_END) -> This now reads existing alerts too
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5) # Wait for Wazuh to write to disk
                continue
            yield line

def ask_ai(alert_data):
    """Sends telemetry to Llama 3.2."""
    print(f"[*] Sending to {MODEL}...")
    prompt = f"Summarize this security alert in 2 sentences for a manager: {alert_data}"
    
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=30)
        return response.json().get("response", "No response.")
    except Exception as e:
        return f"AI Error: {str(e)}"

def monitor_alerts():
    print(f"[*] AI Analyst Active. Scanning {LOG_FILE}...")
    for line in tail_file(LOG_FILE):
        try:
            alert = json.loads(line)
            rule_id = str(alert.get("rule", {}).get("id"))
            
            # PROOF OF LIFE: This tells you the script is actually reading logs
            print(f"[DEBUG] Found Alert ID: {rule_id}", end='\r') 

            if rule_id == TARGET_RULE:
                print(f"\n\n[!] MATCH FOUND: Rule {rule_id} Detected!")
                summary = ask_ai(line)
                print(f"\n[AI REPORT]:\n{summary}\n")
                print("-" * 50)
                print("[*] Resuming scan...")
        except (json.JSONDecodeError, KeyError):
            continue

if __name__ == "__main__":
    monitor_alerts()