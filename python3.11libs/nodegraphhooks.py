import hou
from canvaseventtypes import *
import nodegraphdisplay as display
from hc import Session, NetworkEditor
# import nodegraphview as view


def createEventHandler(uievent, pending_actions):

    if isinstance(uievent, ContextEvent):
        # editor = NetworkEditor(uievent.editor)
        # editor.showPathMessage()
        # return None, True
        return None, False

    elif isinstance(uievent, MouseEvent):
        return None, False

    elif isinstance(uievent, KeyboardEvent) and \
    uievent.eventtype == 'keyhit':
        editor = NetworkEditor(uievent.editor)
        session = Session()
        keymap = {
            # Zoom
            '=': lambda: editor.zoom('in'),
            '-': lambda: editor.zoom('out'),
            # Move view
            'K': lambda: editor.translateView('up'),
            'J': lambda: editor.translateView('down'),
            'H': lambda: editor.translateView('left'),
            'L': lambda: editor.translateView('right'),
            # Move node
            'Alt+K': lambda: editor.translateNodes('up'),
            'Alt+J': lambda: editor.translateNodes('down'),
            'Alt+H': lambda: editor.translateNodes('left'),
            'Alt+L': lambda: editor.translateNodes('right'),
            # Organize
            'Ctrl+Shift+A': editor.arrangeNodes,
            # Grid
            'Shift+G': editor.toggleGridMode,
            # Selection
            'Ctrl+D': editor.pwd().deselectAll
        }

        key = uievent.key
        if key in keymap:
            func = keymap[key]()
            return None, True
        else:
            return None, False

    else:
        return None, False
