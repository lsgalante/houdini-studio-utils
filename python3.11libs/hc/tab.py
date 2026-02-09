import hou
import types


class Tab():
    def __init__(self, hou_tab):
        self.hou_tab = hou_tab

    #
    # Tab
    #

    def close(self):
        self.hou_tab.close()

    def closeOtherTabs(self):
        for tab in self.pane().allTabs():
            if tab != self.tab:
                tab.close()

    def pane(self):
        from .pane import Pane
        return Pane(self.hou_tab.pane())

    def type(self):
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
        return self.hou_tab.hasNetworkControls()

    def isPin(self):
        return self.hou_tab.isPin()
    
    def isShowingNetworkControls(self):
        value = self.hou_tab.isShowingNetworkControls()
        return value

    def setPin(self, value):
        self.hou_tab.setPin(value)
    
    def showNetworkControls(self, value):
        self.hou_tab.showNetworkControls(value)
    
    def toggleNetworkControls(self):
        if self.hasNetworkControls():
            self.showNetworkControls(not self.isShowingNetworkControls())

    def togglePin(self):
        self.setPin(not self.isPin())

