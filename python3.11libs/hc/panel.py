import hou, inspect
from PySide6        import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from fuzzyfinder    import fuzzyfinder
from .session       import Session
from .pane          import Pane
from .tab           import Tab
from importlib      import reload


class Panel(QtWidgets.QDialog):
    def __init__(self):
        super(Panel, self).__init__(hou.qt.mainWindow())

        # Style
        self.resize(900, 400)
        self.setWindowTitle("Panel")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        # Context
        self.session = Session()
        self.tab = self.session.currentTab()
        self.pane = self.tab.pane()
        self.map = {}
        type = self.tab.type()
        print("\n###\nPanel Context: " + str(type) + "\n###")
        if type == "Tab":
            self.map = self.baseMap()
        elif type == "PathTab":
            self.map = self.baseMap() | self.pathTabMap()
        elif type == "NetworkEditor":
            self.map = self.baseMap() | self.pathTabMap() | self.networkEditorMap()
        elif type == "SceneViewer":
            self.map = self.baseMap() | self.pathTabMap() | self.sceneViewerMap()

        # Function list
        self.function_list = FunctionList()
        self.populate()
        self.function_list.setIndex(0)
        # Signals
        self.function_list.itemClicked.connect(self.exec)
        self.function_list.setSelectionMode(QtWidgets.QListWidget.SingleSelection)

        # Input line
        self.input_line = QtWidgets.QLineEdit()
        # Signals
        self.input_line.returnPressed.connect(self.exec)
        self.input_line.textEdited.connect(self.function_list.filter)
        # Set focus

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.function_list)
        self.layout.addWidget(self.input_line)
        self.setLayout(self.layout)

        # Do this last I guess
        self.input_line.setFocus()

    def closeEvent(self, event):
        self.setParent(None)

    def keyPressEvent(self, event):
        key = event.key()
        mod = event.modifiers()

        if key == Qt.Key_Up:
            self.function_list.selectPrevious()
            return
        elif key == Qt.Key_Down:
            self.function_list.selectNext()
            return
        elif key == Qt.Key_P and mod == Qt.ControlModifier:
            self.function_list.selectPrevious()
            return
        elif key == Qt.Key_N and mod == Qt.ControlModifier:
            self.function_list.selectNext()
            return

        super().keyPressEvent(event)

    def exec(self):
        items = self.function_list.items()
        index = items.index(self.function_list.currentItem())
        item = items[index]
        function = self.map[item.text()]
        function()

    def populate(self):
        items = []
        for key in self.map:
            items.append(key)
        self.function_list.addItems(items)

    def baseMap(self):
        return {
            "Close Other Tabs":          self.tab.closeOtherTabs,
            "Close Tab":                 self.tab.close,
            "Color Editor":              self.session.colorEditor,
            "Contract Pane":             self.pane.contract,
            "Expand Pane":               self.pane.expand,
            "Floating Parameter Editor": self.session.floatingParameterEditor,
            "Hide Shelf":                self.session.hideShelf,
            "Maximize Pane":             self.pane.toggleMaximize,
            "Next Tab":                  self.pane.nextTab,
            "Open File":                 self.session.openFile,
            "Open Preferences":          self.session.openPreferences,
            "Previous Tab":              self.pane.previousTab,
            "Reload Colors":             self.session.reloadColorSchemes,
            "Reload Hotkeys":            self.session.reloadHotkeys,
            "Reload Keycam":             self.session.reloadKeycam,
            "Rename Tabs":               self.session.renameTabs,
            "Save":                      self.session.save,
            "Set Type Network Editor":   self.tab.setTypeNetworkEditor,
            "Set Type Parameters":       self.tab.setTypeParm,
            "Set Type Python Shell":     self.tab.setTypePythonShell,
            "Set Type Scene Viewer":     self.tab.setTypeSceneViewer,
            "Set Type Spreadsheet":      self.tab.setTypeDetailsView,
            "Show Shelf":                self.session.showShelf,
            "Split Rotate":              self.pane.splitRotate,
            "Split Swap":                self.pane.splitSwap,
            "Toggle all Menus":          self.session.toggleMenus,
            "Toggle All Paths":          self.session.toggleNetworkControls,
            "Toggle All Tabs":           self.session.toggleTabs,
            "Toggle Autosave":           self.session.toggleAutoSave,
            "Toggle Main Menu":          self.session.toggleMainMenu,
            "Toggle Stowbars":           self.session.toggleStowbars,
            "Toggle Tabs":               self.pane.toggleTabs,
            "Toggle Update Mode":        self.session.toggleUpdateMode,
            "Update Mode: Auto":         self.session.setUpdateModeAuto,
            "Update Mode: Manual":       self.session.setUpdateModeManual
        }

    def sceneViewerMap(self):
        return {
            "Frame":                self.tab.frame,
            "Home Viewports":       self.tab.homeAllViewports,
            "Keycam":               self.tab.keycam,
            "Toggle Backface":      self.tab.toggleBackface,
            "Toggle Bars":          self.tab.toggleBars,
            "Toggle Display Bar":   self.tab.toggleDisplayBar,
            "Toggle Grid":          self.tab.toggleGrid,
            "Toggle Group List":    self.tab.toggleGroupList,
            "Toggle Light Geo":     self.tab.toggleLightGeo,
            "Toggle Operation Bar": self.tab.toggleOperationBar,
            "Toggle Point Markers": self.tab.togglePointMarkers,
            "Toggle Point Normals": self.tab.togglePointNormals,
            "Toggle Point Numbers": self.tab.togglePointNumbers,
            "Toggle Prim Normals":  self.tab.togglePrimNormals,
            "Toggle Prim Numbers":  self.tab.togglePrimNumbers,
            "ToggleSelectionBar":   self.tab.toggleSelectionBar,
            "Toggle Vectors":       self.tab.toggleVectors
        }

    def pathTabMap(self):
        return {
            "Toggle Path": self.tab.toggleNetworkControls,
            "Toggle Pin":  self.tab.togglePin
        }

    def networkEditorMap(self):
        return {
            "Arrange Nodes":     self.tab.arrangeNodes,
            "Deselect All":      self.tab.pwd().deselectAll,
            "Frame All":         self.tab.frameAll,
            "Rename Node":       self.tab.renameNode,
            "Set Node Colors":   self.tab.setNodeColors,
            "Set Node Shapes":   self.tab.setNodeShapes,
            "Show Path Message": self.tab.showPathMessage,
            "Toggle Grid Mode":  self.tab.toggleGridMode,
            "Toggle Menu":       self.tab.toggleMenu
            # "Show Radial Menu":  self.tab.showRadialMenu,
        }


class FunctionList(QtWidgets.QListWidget):
    def currentItem(self):
        return self.selectedItems()[0]

    def filter(self, query):
        items = self.items()
        item_names = [item.text() for item in items]
        matches = list(fuzzyfinder(query, item_names))
        for item in items:
            if item.text() in matches:
                item.setHidden(0)
            else:
                item.setHidden(1)
        self.setIndex(0)

    def items(self):
        items = []
        for i in range(self.count()):
            items.append(self.item(i))
        return(items)

    def selectNext(self):
        items = self.visibleItems()
        index = items.index(self.currentItem())
        index = (index + 1) % len(items)
        self.setIndex(index)

    def selectPrevious(self):
        items = self.visibleItems()
        index = items.index(self.currentItem())
        index = (index - 1) % len(items)
        self.setIndex(index)

    def setIndex(self, index):
        counter = 0
        for item in self.visibleItems():
            if counter == index:
                self.setCurrentItem(item)
            counter += 1

    def visibleItems(self):
        items = []
        for i in range(self.count()):
            item = self.item(i)
            if not item.isHidden():
                items.append(item)
        return(items)


# class InputLine(QtWidgets.QLineEdit):

