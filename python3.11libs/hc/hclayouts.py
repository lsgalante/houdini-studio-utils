from .hcsession import HCSession

def setLayoutQuad(self):
    hc_session = HCSession()
    hc_session.clearLayout()
    hc_session.allTabs()[0].setType("PythonShell")
    hc_session.allPanes()[0].splitHorizontal()
    hc_session.allPanes()[0].splitVertical()
    hc_session.allPanes()[1].splitVertical()

def setLayoutRamp(self):
    hc_session = HCSession()
    hc_session.removeEventLoopCallbacks()
    hc_session.clearLayout()
    hc_session.allPanes()[0].splitVertical()
    hc_session.allTabs()[1].setType("Parm")
    hc_session.allPanes()[1].setSplitRatio(0.3)
    hc_session.allPanes()[1].createTab()

def setLayoutTriH(self):
    hc_session = HCSession()
    hc_session.removeEventLoopCallbacks()
    hc_session.clearLayout()
    # Make panes
    hc_session.allTabs()[0].setType("PythonShell")
    hc_session.allPanes()[0].splitHorizontal()
    hc_session.allPanes()[1].splitHorizontal()
    # Make tabs
    hc_session.allPanes()[1].createTab("PythonShell")
    hc_session.allPanes()[1].allTabs()[0].setIsCurrentTab()
    # Set types
    hc_session.allPanes()[0].allTabs()[0].setType("SceneViewer")
    hc_session.allPanes()[1].allTabs()[0].setType("Parm")
    hc_session.allPanes()[1].allTabs()[1].setType("DetailsView")
    hc_session.allPanes()[2].allTabs()[0].setType("NetworkEditor")
    # Ratios
    hc_session.allPanes()[0].setSplitFraction(0.5)
    hou.session.last_pane = self.pane()
    hou.ui.addEventLoopCallback(triHCallback)

def triHCallback(session):
    panes = session.panes()
    pane = session.pane()
    if str(pane) != str(hou.session.lastPane):
        hou.session.last_pane = pane
        if str(pane) == str(panes[1]):
            pane.setSplitFraction(0.6)
        elif str(pane) == str(panes[2]):
            pane.setSplitFraction(0.3)
    return True

def setLayoutTriV(session):
    # Remove callbacks
    session.removeEventLoopCallbacks()
    # Reset layout
    session.clearLayout()
    # Make panes
    session.allPanes()[0].allTabs()[0].setType("PythonShell")
    session.allPanes()[0].splitHorizontal()
    session.allPanes()[1].splitVertical()
    # Make pane tabs
    session.allPanes()[1].createTab("PythonShell")
    session.allPanes()[1].allTabs()[0].setIsCurrentTab()
    # Set types
    session.allPanes()[0].allTabs()[0].setType("SceneViewer")
    session.allPanes()[1].allTabs()[0].setType("Parm")
    session.allPanes()[1].allTabs()[1].setType("DetailsView")
    session.allPanes()[2].allTabs()[0].setType("NetworkEditor")
    # Set ratios
    session.allPanes()[0].setSplitFraction(0.66)
    # Ok
    hou.session.last_pane = self.pane()
    hou.ui.addEventLoopCallback(self.triVCallback)

def triVCallback(session):
    panes = session.allPanes()
    pane = session.currentPane()
    if str(pane) != str(hou.session.last_pane):
        hou.session.last_pane = pane
        if str(pane) == str(panes[0]):
            pane.setSplitFraction(0.7)
        elif str(pane) == str(panes[1]):
            panes[0].setSplitFraction(0.4)
            pane.setSplitFraction(0.33)
        elif str(pane) == str(panes[2]):
            panes[0].setSplitFraction(0.4)
            pane.setSplitFraction(0.66)
    return True
