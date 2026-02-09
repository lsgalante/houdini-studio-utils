import hou
from .tab           import Tab
from .pathtab       import PathTab
from .sceneviewer   import SceneViewer
from .networkeditor import NetworkEditor


class Pane:
    def __init__(self, hou_pane):
        self.hou_pane = hou_pane


    """ Pane """

    def close(self):
        for tab in self.allTabs():
            tab.close()

    def isMaximized(self):
        return self.hou_pane.isMaximized()

    def qtScreenGeometry(self):
        return self.hou_pane.qtScreenGeometry()

    def setIsMaximized(self, bool):
        self.hou_pane.setIsMaximized(bool)

    def toggleMaximize(self):
        self.hou_pane.setIsMaximized(not self.isMaximized())


    """ Split """

    def contract(self):
        fraction = round(self.splitFraction(), 3) + 0.1
        self.setSplitFraction(fraction)
        hou.ui.setStatusMessage("Pane fraction: " + str(fraction))

    def expand(self):
        fraction = round(self.splitFraction(), 3) - 0.1
        self.setSplitFraction(fraction)
        hou.ui.setStatusMessage("Pane fraction: " + str(fraction))

    def isSplitMaximized(self):
        return self.hou_pane.isSplitMaximized()

    def setIsSplitMaximized(self, bool):
        self.hou_pane.setIsSplitMaximized(bool)

    def setRatioHalf(self):
        self.setSplitFraction(0.5)

    def setRatioQuarter(self):
        self.setSplitFraction(0.25)

    def setRatioThird(self):
        self.setSplitFraction(0.333)

    def setSplitFraction(self, fraction):
        self.hou_pane.setSplitFraction(fraction)

    def splitFraction(self):
        return self.hou_pane.getSplitFraction()

    def splitHorizontal(self):
        self.hou_pane.splitHorizontally()

    def splitRotate(self):
        self.hou_pane.splitRotate()

    def splitSwap(self):
        self.hou_pane.splitSwap()

    def splitVertical(self):
        self.hou_pane.splitVertically()

    def toggleSplitMaximized(self):
        self.setIsSplitMaximized(not self.isSplitMaximized())


    """ Interface """

    def allTabs(self):
        tabs = []
        for hou_tab in self.hou_pane.tabs():
            tabs.append(self.convertTab(hou_tab))
        return tabs

    def convertTab(self, hou_tab):
        hou_type = hou_tab.type()
        if hou_type == hou.paneTabType.SceneViewer:
            return SceneViewer(hou_tab)
        elif hou_type == hou.paneTabType.NetworkEditor:
            return NetworkEditor(hou_tab)
        elif hou_type == hou.paneTabType.DetailsView:
            return PathTab(hou_tab)
        elif hou_type == hou.paneTabType.Parm:
            return PathTab(hou_tab)
        else:
            return Tab(hou_tab)

    def currentTab(self):
        hou_tab = self.hou_pane.currentTab()
        return self.convertTab(hou_tab)

    def isShowingTabs(self):
        return self.hou_pane.isShowingPaneTabs()

    def nextTab(self):
        tabs = self.hou_pane.tabs()
        tab = self.hou_pane.currentTab()
        index = tabs.index(tab)
        index = (index + 1) % len(tabs)
        tabs[index].setIsCurrentTab()

    def previousTab(self):
        tabs = self.hou_pane.tabs()
        tab = self.hou_pane.currentTab()
        index = tabs.index(tab)
        index = (index - 1) % len(tabs)
        tabs[index].setIsCurrentTab()

    def showTabs(self, value):
        self.hou_pane.showPaneTabs(value)

    def toggleTabs(self):
        self.showTabs(not self.isShowingTabs())
