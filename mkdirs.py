import os
from pathlib import Path

calls_log = Path("mkdirs_example/output")/"open_ai_calls.json"
if not calls_log.exists():
    os.makedirs(calls_log)