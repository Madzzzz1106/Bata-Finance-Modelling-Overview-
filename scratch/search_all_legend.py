import os
import json

logs_dir = "/Users/mridulagarwal/.gemini/antigravity-ide/brain/f4ddb366-fe61-4ecb-83dd-a205e786c4c2/.system_generated/logs"
transcript_path = os.path.join(logs_dir, "transcript.jsonl")

if os.path.exists(transcript_path):
    print("Searching transcript for 'legend'...")
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                content = obj.get("content", "")
                if "legend" in content.lower():
                    print(f"Step {obj.get('step_index')}:")
                    # print lines containing legend
                    for l in content.split("\n"):
                        if "legend" in l.lower():
                            print("  ", l)
            except:
                pass
