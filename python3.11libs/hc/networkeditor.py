import hou, math, types
from .pathtab import PathTab
from .prefs import Prefs


class NetworkEditor(PathTab):
    def __init__(self, hou_tab):
        self.hou_tab = hou_tab
        self.delta_t = 2

    """ Move network objects """

    def arrangeNodes(self):
        return

    def snapToGrid(self, node):
        P = node.position()
        P[0] = round(P[0] - 0.5) + 0.5
        P[1] = round(P[1] - 0.85) + 0.85
        node.setPosition(P)

    def translateNodes(self, direction):
        for node in self.pwd().selectedChildren():
            self.snapToGrid(node)
            P = node.position()
            # do the move
            if direction == 'up':
                P[1] += 1
            elif direction == 'down':
                P[1] -= 1
            elif direction == 'left':
                P[0] -= 1
            elif direction == 'right':
                P[0] += 1
            node.setPosition(P)

    """ Viewport """

    def bounds(self):
        return self.hou_tab.visibleBounds()

    def cursorPosition(self):
        return self.hou_tab.cursorPosition()

    def frameAll(self):
        self.hou_tab.requestZoomReset()

    def screenSize(self):
        return self.hou_tab.screenBounds().size()

    def size(self):
        return self.bounds().size()

    def setBounds(self, bounds):
        self.hou_tab.setVisibleBounds(bounds)

    def translateView(self, direction):
        xform_map = {
            'up':    hou.Vector2(0, self.delta_t * self.zoomLevel()),
            'down':  hou.Vector2(0, self.delta_t * self.zoomLevel() * -1),
            'left':  hou.Vector2(self.delta_t * self.zoomLevel() * -1, 0),
            'right': hou.Vector2(self.delta_t * self.zoomLevel(), 0)
        }
        bounds = self.bounds()
        bounds.translate(xform_map[direction])
        self.setBounds(bounds)

    def zoom(self, direction):
        scalemap = {
            'in':  (0.75, 0.75),
            'out': (1.25, 1.25)
        }
        bounds = self.bounds()
        bounds.scale(scalemap[direction])
        self.setBounds(bounds)

    def zoomLevel(self):
        zoomlevel = self.size()[0] / self.size()[0]
        return zoomlevel

    """ Interface states & utils """

    def isMenuOpen(self):
        value = self.hou_tab.getPref('showmenu')
        return int(value)

    def setMenuOpen(self, value):
        self.hou_tab.setPref('showmenu', str(value))

    def showPathMessage(self):
        self.hou_tab.flashMessage(image=None, message=self.path(), duration=1)

    # def showRadialMenu(self):
        # from .radialutils import editorRadialMain
        # menu = editorRadialMain()
        # self.hou_tab.displayRadialMenu("hc_editor_radial_menu")

    def toggleDimUnusedNodes(self):
        map = {
            '0': '1',
            '1': '0'
        }
        mode = self.hou_tab.getPref('dimunusednodes')
        self.hou_tab.setPref('dimunusednodes', map[mode])

    def toggleGridMode(self):
        map = {
            '0': '1',
            '1': '2',
            '2': '0'
        }
        mode = self.hou_tab.getPref('gridmode')
        self.hou_tab.setPref('gridmode', map[mode])

    def toggleMenu(self):
        map = {
            '0': '1',
            '1': '0'
        }
        mode = self.hou_tab.getPref('showmenu')
        self.hou_tab.setPref('showmenu', map[mode])

    """ Utility """

    def type(self):
        return "NetworkEditor"

    def renameNode(self):
        node = self.currentNode()
        name = hou.ui.readInput("Rename_node", buttons=("Yes", "No"))
        if name[0] == 0:
            node.setName(name[1])

    def setNodeColors(self):
        color = hou.ui.selectColor(hou.Color(Prefs().node_color))
        nodes = self.pwd().selectedChildren()
        for node in nodes:
            node.setColor(color)

    def setNodeShapes(self):
        nodes = self.pwd().children()
        for node in nodes:
            node.setUserData("nodeshape", "rect")
