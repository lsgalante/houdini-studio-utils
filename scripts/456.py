from pathlib import Path
import hou
import json

# This file runs when a .hip file is loaded

current_file = hou.hipFile.path() 
state_file = Path(hou.getenv("HOUDINI_USER_PREF_DIR")) / "st_data" / "state.json"
data = {"last_opened_file": current_file}

# Write to JSON
updates = {"last_file": current_file}
with open(state_file, 'w') as f:
    json.dump(updates, f, indent=4)
