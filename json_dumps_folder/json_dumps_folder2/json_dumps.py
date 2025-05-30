# you have to run this file by going to the root directory and doing python main_for_json_dumps.py
import json
import os
import random
from pathlib import Path

# from json_dumps_folder.test import test_var
# OR
from ..test import test_var

print("starting app")
print(test_var)

calls_log = Path("data_folder/output") / "open_ai_calls.json"
print("""*Example calls_log:\n""", calls_log)

log_entry = {"model": random.randint(1, 10)}

# 1. Check if the directory exists, if not create it
if not calls_log.exists():
    print("doesnt exist")
    with open(calls_log, "w", encoding="utf-8") as f:
        json.dump([log_entry], f)
        print(f"Log entry written to new file: {calls_log}")
# 2. If the directory exists, load it and append the new entry, then
else:
    with open(calls_log, "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            print("JSONDecodeError: File is empty or corrupted.")
            existing_data = []

    with open(calls_log, "w", encoding="utf-8") as f:
        existing_data.append(log_entry)
        f.seek(0)
        f.truncate()
        try:
            # f.write("aaaaaaaaaaaaaa")
            json.dump(existing_data, f, indent=4)
            print(f"Log entry written to file: {calls_log}")
        except Exception as e:
            print(f"Error writing log entry to file: {str(e)}")
            raise
