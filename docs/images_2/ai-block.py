#!/usr/bin/env python3
import sys
import json
import subprocess
import time
from datetime import datetime

# LOG FILE: This is where we write to Terminal 3
LOG_FILE = "/var/ossec/logs/active-responses.log"

def write_log(msg):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
        f.write(f"{timestamp} {msg}\n")

def main():
    try:
        # 1. Read the input from Wazuh (JSON format)
        input_data = sys.stdin.read()
        if not input_data:
            write_log("ai-block.py: ERROR - No input received from Wazuh")
            sys.exit(1)

        alert = json.loads(input_data)
        
        # 2. Extract the Source IP
        # Wazuh 4.x structure: parameters -> alert -> data -> srcip
        try:
            srcip = alert['parameters']['alert']['data']['srcip']
            command = alert['command']
        except KeyError:
            # Fallback for older rule structures
            srcip = alert.get('srcip') or "0.0.0.0"
            command = "add"

        if srcip == "0.0.0.0" or srcip == "127.0.0.1":
            write_log("ai-block.py: INFO - Skipping invalid or localhost IP")
            sys.exit(0)

        # 3. Execute the Block (ADD)
        if command == "add":
            # Check if already blocked to avoid duplicates
            check = subprocess.run(["iptables", "-C", "INPUT", "-s", srcip, "-j", "DROP"], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if check.returncode != 0:
                subprocess.run(["iptables", "-I", "INPUT", "1", "-s", srcip, "-j", "DROP"])
                write_log(f"active-response/bin/ai-block.py: add - {srcip}")
            else:
                write_log(f"active-response/bin/ai-block.py: INFO - IP {srcip} already blocked")

        # 4. Unblock (DELETE) - strictly optional for this test
        elif command == "delete":
            subprocess.run(["iptables", "-D", "INPUT", "-s", srcip, "-j", "DROP"])
            write_log(f"active-response/bin/ai-block.py: delete - {srcip}")

    except Exception as e:
        write_log(f"ai-block.py: CRITICAL ERROR - {str(e)}")

if __name__ == "__main__":
    main()
