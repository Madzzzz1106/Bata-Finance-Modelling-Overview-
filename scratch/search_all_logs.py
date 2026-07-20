import os
import json

brain_dir = "/Users/mridulagarwal/.gemini/antigravity-ide/brain"
if os.path.exists(brain_dir):
    subdirs = [d for d in os.listdir(brain_dir) if os.path.isdir(os.path.join(brain_dir, d))]
    print("Found brain subdirectories:", subdirs)
    
    # Let's search all logs in all conversation subdirectories for 9,610, 17,200, 9k, or 17k
    for sd in subdirs:
        transcript_path = os.path.join(brain_dir, sd, ".system_generated/logs/transcript.jsonl")
        if os.path.exists(transcript_path):
            with open(transcript_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        content = obj.get("content", "")
                        if not content:
                            continue
                        if any(x in content for x in ["9,610", "17,200", "17200", "9610"]):
                            # print match
                            print(f"Match in conv {sd}, Step {obj.get('step_index')}:")
                            print(content[:300] + "...\n")
                    except:
                        pass
else:
    print("Brain dir not found")
