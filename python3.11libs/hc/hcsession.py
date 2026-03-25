import hou
from .hcbindings import HCBindings
from .hcnetworkeditor import HCNetworkEditor
from .hcsceneviewer import HCSceneViewer
from .hcpane import HCPane
from .hcpathtab import HCPathTab
from .hctab import HCTab


class Session:
    def __init__(self):
        return

    """ Context """

    def currentNode(self):
        return self.currentHCTab().currentNode()

    def projectPath(self):
        return hou.hipFile.path()


    """
    Layout
    'allTabs' and 'currentTab' do not use hou.ui.paneTabUnderCursor method
    """

    def allHCNetworkEditors(self):
        hc_network_editors = []
        for hc_tab in self.allHCTabs():
            if hc_tab.type() == "NetworkEditor":
                hc_network_editors.append(tab)
        return hc_network_editors

    def allHCPanes(self):
        hc_panes = []
        for pane in self.desktop().panes():
            hc_panes.append(HCPane(pane))
        return panes

    def allHCSceneViewers(self):
        hc_scene_viewers = []
        for tab in self.allTabs():
            if tab.type() == "SceneViewer":
                viewers.append(SceneViewer(tab))
        return viewers

    def allHCTabs(self):
        tabs = []
        for pane in self.allPanes():
            for tab in pane.allTabs():
                tabs.append(tab)
        return tabs

    def allHCViewports(self):
        hc_viewports = []
        hc_scene_viewers = self.allHCSceneViewers
        for hc_scene_viewer in hc_scene_viewers:
            for hc_viewport in hc_scene_viewer.allHCCiewports():
                hc_viewports.append(hc_viewport)
        return hc_viewports

    def clearLayout(self):
        tabs = self.allTabs()
        for tab in tabs:
            if tab != tabs[0]:
                tab.close()

    def currentHCPane(self):
        return HCPane(hou.ui.paneUnderCursor())

    def currentHCTab(self):
        return self.currentHCPane().currentHCTab()

    def desktop(self):
        return hou.ui.curDesktop()

    def printHCLayout(self):
        panes = hou.ui.panes()
        root = panes[0].getSplitParent()
        lefts = []
        tops = []
        for pane in self.panes():
            geo = pane.qtScreenGeometry()
            lefts.append(geo.left())
            tops.append(geo.top())
        print(lefts)
        print(tops)

    def renameTabs(self):
        tabs = hou.ui.paneTabs()
        i = 0
        for tab in tabs:
            tab.setName('placeholder' + str(i))
            i += 1
        i = 0
        for tab in tabs:
            tab.setName('panetab' + str(i))
            i += 1

    def layoutRoot(self):
        root = hou.ui.panes()[0].getSplitParent().getSplitParent()


    """ Settings """

    def isAutoSave(self):
        return hou.getPreference('autoSave')

    def openPreferences(self):
        hou.ui.openPreferences('ui', '')

    def reloadColorSchemes(self):
        hou.ui.reloadColorScheme()
        hou.ui.reloadViewportColorSchemes()

    def reloadHC(self):
        hou.ui.reloadPackage(hou.homeHoudiniDirectory() + '/packages/houdini-studio-utils.json')

    def reloadHotkeys(self):
        HCBindings().load()

    def reloadKeycam(self):
        hou.ui.reloadViewerState('keycam')

    def setUpdateModeAuto(self):
        hou.setUpdateMode(hou.updateMode.AutoUpdate)

    def setUpdateModeManual(self):
        hou.setUpdateMode(hou.updateMode.Manual)

    def triggerUpdate(self):
        hou.ui.triggerUpdate()

    def toggleAutoSave(self):
        map = {'0': '1', '1': '0'}
        hou.setPreference('autoSave', map[hou.getPreference('autoSave')])

    def toggleUpdateMode(self):
        mode_map = {
            "updateMode.AutoUpdate": hou.updateMode.Manual,
            "updateMode.Manual": hou.updateMode.AutoUpdate
        }
        hou.setUpdateMode(mode_map(str(hou.updateModeSetting)))

    def updateMainMenuBar(self):
        hou.ui.updateMainMenuBar()


    """ Utils """

    def colorEditor(self):
        hou.ui.selectColor()

    def keycam(self):
        msgmap = {
            "Object": "Entered keycam in an obj/object context",
            "Sop": "Entered keycam in a sop/geometry context",
            "Lop": "Entered keycam in a lop context"
        }
        viewer = self.sceneViewers()[0]
        category = viewer.pwd().childTypeCategory().name()
        if category in msgmap:
            viewer.setCurrentState('keycam')
            hou.ui.setStatusMessage(msgmap[category])
        else:
            hou.ui.setStatusMessage("Keycam is only available in obj, sop and lop contexts",
                hou.severityType.Error)

    def openFile(self):
        file = hou.ui.selectFile()
        hou.hipFile.load(file)

    def removeEventLoopCallbacks(self):
        callbacks = hou.ui.eventLoopCallbacks()
        for callback in callbacks:
            hou.ui.removeEventLoopCallback(callback)

    # def restartHoudini(self):
        # import os
        # import subprocess
        # executable = sys.argv[0]
        # executable = os.environ.get("HFS") + "/bin/houdini"
        # subprocess.Popen([executable])
        # hou.exit()
        # return

    def save(self):
        hou.hipFile.save()


    """ Interface """

    def isVisibleMainMenu(self):
        value = hou.getPreference('showmenu.val')
        return int(value)

    def isVisibleMenus(self):
        visible = 0
        panes = self.allPanes()
        tabs = self.allTabs()
        # Main menu
        if self.isVisibleMainMenu():
            visible = 1
        # Tabs
        for tab in tabs:
            if tab.type() == "NetworkEditor":
                if tab.isMenuOpen():
                    visible = 1
                elif tab.isShowingNetworkControls():
                    visible = 1
            elif tab.type() == "PathTab":
                if tab.isShowingNetworkControls():
                    visible = 1
            elif tab.type() == "SceneViewer":
                if tab.isShowingNetworkControls():
                    visible = 1
                elif tab.isVisibleOperationBar():
                    visible = 1
                elif tab.isVisibleDisplayBar():
                    visible = 1
                elif tab.isVisibleSelectionBar():
                    visible = 1
        # Panes
        for pane in panes:
            if pane.isShowingTabs():
                visible = 1
        return visible

    def floatingParameterEditor(self):
        tab = self.currentTab()
        if tab.type() == "NetworkEditor":
            hou.ui.showFloatingParameterEditor(self.currentNode())
        else:
            hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)

    def hideShelf(self):
        self.desktop().shelfDock().show(0)

    def showMainMenu(self, value):
        hou.setPreference('showmenu.val', str(value))

    def showShelf(self):
        self.shelfDock().show(1)

    def toggleMainMenu(self):
        value = (self.isVisibleMainMenu()+1) % 2
        self.showMainMenu(value)

    def toggleMenus(self):
        visible = self.isVisibleMenus()
        panes = self.allPanes()
        tabs = self.allTabs()
        # Set state
        self.showMainMenu((visible+1) % 2)
        for tab in tabs:
            if tab.type() == "NetworkEditor":
                tab.showNetworkControls(not visible)
                tab.setMenuOpen(0)
            elif tab.type() == "PathTab":
                tab.showNetworkControls(not visible)
            elif tab.type() == "SceneViewer":
                tab.showNetworkControls(not visible)
                tab.showOperationBar(not visible)
                tab.showDisplayBar(not visible)
                tab.showSelectionBar(not visible)
        for pane in panes:
            pane.showTabs(not visible)
        # Apply (needs to be called twice for some reason)
        # hou.ui.setHideAllMinimizedStowbars(visible)
        # hou.ui.setHideAllMinimizedStowbars(visible)

    def toggleNetworkControls(self):
        visible = 0
        tabs = self.allTabs()
        for tab in tabs:
            if tab.isShowingNetworkControls():
                visible = 1
        for tab in tabs:
            tab.showNetworkControls(not visible)

    def toggleStowbars(self):
        if hou.ui.hideAllMinimizedStowbars():
            hou.ui.setHideAllMinimizedStowbars(False)
        else:
            hou.ui.setHideAllMinimizedStowbars(True)
            hou.ui.setHideAllMinimizedStowbars(True)

    def toggleTabs(self):
        visible = 0
        panes = self.allPanes()
        for pane in panes:
            if pane.isShowingTabs():
                visible = 1
        for pane in panes:
            pane.showTabs(not visible)
