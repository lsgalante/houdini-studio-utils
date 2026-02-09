from pathlib import Path
import hou
import json

# This file runs when houdini is opened without a .hip file

# Check/create st_data directory
data_dir = Path(hou.getenv("HOUDINI_USER_PREF_DIR")) / "st_data"
data_dir.mkdir(parents=True, exist_ok=True)

# Check/create state.json file
state_file = data_dir / "state.json"

if not state_file.exists():
    defaults = {
        "last_file": ""
    }

    with open(state_file, 'w') as f:
        json.dump(defaults, f, indent=4)

else:
    with open(state_file, 'r') as f:
        loaded_state = json.load(f)
        last_file = loaded_state['last_file']
        if last_file != "":
            choice = hou.ui.displayCustomConfirmation(
                text=f"Open last file {last_file}?",
                buttons=("Yes", "No"),
                suppress=hou.confirmType.NoConfirmType
            )
            if choice == 0:
                hou.hipFile.load(last_file)

