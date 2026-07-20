import json
import os
import re

logs_dir = "/Users/mridulagarwal/.gemini/antigravity-ide/brain/ccd9cf54-90b6-44e0-a812-07bb78a70a56/.system_generated/logs"
transcript_path = os.path.join(logs_dir, "transcript.jsonl")

if os.path.exists(transcript_path):
    print("Transcript found! Searching...")
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                content = obj.get("content", "")
                if not content:
                    continue
                # search for patterns
                if any(x in content for x in ["9,610", "17,200", "9k", "17k", "market cap", "capitalization"]):
                    print(f"Step {obj.get('step_index')}: {obj.get('type')} by {obj.get('source')}")
                    print(content[:300] + "...\n")
            except Exception as e:
                pass
else:
    print(f"Transcript not found at {transcript_path}")
