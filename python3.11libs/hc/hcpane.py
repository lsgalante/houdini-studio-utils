import hou
from .hctab           import HCTab
from .hcpathtab       import HCPathTab
from .hcsceneviewer   import HCSceneViewer
from .hcnetworkeditor import HCNetworkEditor

class HCPane:
    def __init__(self, pane):
        self.pane = pane

    """ Pane """

    def close(self):
        for hc_tab in self.allHCTabs():
            hc_tab.close()

    def isMaximized(self):
        return self.pane.isMaximized()

    def qtScreenGeometry(self):
        return self.pane.qtScreenGeometry()

    def setIsMaximized(self, bool):
        self.pane.setIsMaximized(bool)

    def toggleMaximize(self):
        self.pane.setIsMaximized(not self.isMaximized())


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
        return self.pane.isSplitMaximized()

    def setIsSplitMaximized(self, bool):
        self.pane.setIsSplitMaximized(bool)

    def setRatioHalf(self):
        self.setSplitFraction(0.5)

    def setRatioQuarter(self):
        self.setSplitFraction(0.25)

    def setRatioThird(self):
        self.setSplitFraction(0.333)

    def setSplitFraction(self, fraction):
        self.pane.setSplitFraction(fraction)

    def splitFraction(self):
        return self.pane.getSplitFraction()

    def splitHorizontal(self):
        self.pane.splitHorizontally()

    def splitRotate(self):
        self.pane.splitRotate()

    def splitSwap(self):
        self.pane.splitSwap()

    def splitVertical(self):
        self.pane.splitVertically()

    def toggleSplitMaximized(self):
        self.setIsSplitMaximized(not self.isSplitMaximized())


    """ Interface """

    def allHCTabs(self):
        hc_tabs = []
        for tab in self.pane.tabs():
            hc_tabs.append(HCTab(tab))
        return hc_tabs

    def convertTab(self, tab):
        tab_type = tab.type()
        if tab_type == hou.paneTabType.SceneViewer:
            return HCSceneViewer(tab)
        elif tab_type == hou.paneTabType.NetworkEditor:
            return HCNetworkEditor(tab)
        elif tab_type == hou.paneTabType.DetailsView:
            return HCPathTab(tab)
        elif tab_type == hou.paneTabType.Parm:
            return HCPathTab(tab)
        else:
            return HCTab(tab)

    def currentHCTab(self):
        tab = self.pane.currentTab()
        return self.convertTab(tab)

    def isShowingTabs(self):
        return self.pane.isShowingPaneTabs()

    def nextTab(self):
        tabs = self.pane.tabs()
        tab = self.pane.currentTab()
        index = tabs.index(tab)
        index = (index + 1) % len(tabs)
        tabs[index].setIsCurrentTab()

    def previousTab(self):
        tabs = self.pane.tabs()
        tab = self.pane.currentTab()
        index = tabs.index(tab)
        index = (index - 1) % len(tabs)
        tabs[index].setIsCurrentTab()

    def showTabs(self, value):
        self.pane.showPaneTabs(value)

    def toggleTabs(self):
        self.showTabs(not self.isShowingTabs())
