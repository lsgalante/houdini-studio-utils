import hou
import json
from pathlib import Path

"""
KEY NAMES
uparrow, downarrow, leftarrow, rightarrow
alt, cmd, shift, ctrl, tab, del, backspace, enter, esc
f1...f12
pageup, pagedown, end, home, insert
/, \
pad0...pad9
padstar, padslash
pause
space
"""

class HCBindings:
    def __init__(self):
        return

    def load(self):
        self.clear()
        self.assign()

    def clear(self):
        path = Path(hou.getenv("HC_PATH"))
        file = path / "scripts" / "hotkeys_clear.json"
        data = json.loads(file.read_text())
        commands = data.get("commands")
        for command in commands:
            context = command.rpartition('.')[0]
            hou.hotkeys.clearAssignments(context, command)

    def assign(self):
        path = Path(hou.getenv("HC_PATH"))
        file = path / "scripts" / "hotkeys_assign.json"
        data = json.loads(file.read_text())
        assignments = data.get("assignments")
        for symbol, key in assignments.items():
            context = symbol.rpartition('.')[0]
            hou.hotkeys.addAssignment(context, symbol, key)

    def bindCommands(self):
        list = ()
        for command in list:
            context = binding[0]
            command = binding[1]
            hou.hotkeys.addCommandBinding(context, command)
