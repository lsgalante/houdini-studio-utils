import hou
import types
from .hcpane import HCPane

class HCTab():
    def __init__(self, tab):
        self.tab = tab

    #
    # Tab
    #

    def close(self):
        self.tab.close()

    def closeOtherTabs(self):
        for tab in self.hcPane().allTabs():
            if tab != self.tab:
                tab.close()

    def hcPane(self):
        return HCPane(self.tab.pane())

    def hcType(self):
        return "Tab"

    def setTypeDetailsView(self):
        self.setType(hou.paneTabType.DetailsView)

    def setTypeNetworkEditor(self):
        self.setType(hou.paneTabType.NetworkEditor)

    def setTypeParm(self):
        self.setType(hou.paneTabType.Parm)

    def setTypePythonShell(self):
        self.setType(hou.paneTabType.PythonShell)

    def setTypeSceneViewer(self):
        self.setType(hou.paneTabType.SceneViewer)

    def setType(self, type):
        tab = self.tab.setType(type)
        return tab

    #
    # UI
    #

    def hasNetworkControls(self):
        return self.tab.hasNetworkControls()

    def isPin(self):
        return self.tab.isPin()

    def isShowingNetworkControls(self):
        value = self.tab.isShowingNetworkControls()
        return value

    def setPin(self, value):
        self.tab.setPin(value)

    def showNetworkControls(self, value):
        self.tab.showNetworkControls(value)

    def toggleNetworkControls(self):
        if self.hasNetworkControls():
            self.showNetworkControls(not self.isShowingNetworkControls())

    def togglePin(self):
        self.setPin(not self.isPin())

