from .session import Session

def setLayoutQuad(self):
    session = Session()
    session.clearLayout()
    session.allTabs()[0].setType("PythonShell")
    session.allPanes()[0].splitHorizontal()
    session.allPanes()[0].splitVertical()
    session.allPanes()[1].splitVertical()

def setLayoutRamp(self):
    session = Session()
    session.removeEventLoopCallbacks()
    session.clearLayout()
    session.allPanes()[0].splitVertical()
    session.allTabs()[1].setType("Parm")
    session.allPanes()[1].setSplitRatio(0.3)
    session.allPanes()[1].createTab()

def setLayoutTriH(self):
    session = Session()
    session.removeEventLoopCallbacks()
    session.clearLayout()
    # Make panes
    session.allTabs()[0].setType("PythonShell")
    session.allPanes()[0].splitHorizontal()
    session.allPanes()[1].splitHorizontal()
    # Make tabs
    session.allPanes()[1].createTab("PythonShell")
    session.allPanes()[1].allTabs()[0].setIsCurrentTab()
    # Set types
    session.allPanes()[0].allTabs()[0].setType("SceneViewer")
    session.allPanes()[1].allTabs()[0].setType("Parm")
    session.allPanes()[1].allTabs()[1].setType("DetailsView")
    session.allPanes()[2].allTabs()[0].setType("NetworkEditor")
    # Ratios
    session.allPanes()[0].setSplitFraction(0.5)
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
