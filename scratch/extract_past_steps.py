import json
import os

logs_dir = "/Users/mridulagarwal/.gemini/antigravity-ide/brain/f4ddb366-fe61-4ecb-83dd-a205e786c4c2/.system_generated/logs"
transcript_path = os.path.join(logs_dir, "transcript.jsonl")

if os.path.exists(transcript_path):
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                step = obj.get("step_index")
                if step in [219, 220, 221, 222, 223]:
                    print(f"=== STEP {step} ({obj.get('type')} by {obj.get('source')}) ===")
                    print(obj.get("content"))
                    print("\n" + "="*40 + "\n")
            except:
                pass
