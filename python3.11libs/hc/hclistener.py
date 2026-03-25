import hou
from .session import Session
from .pane import Pane
from .tab import Tab


class Listener():
    def __init__(self):
        self.report_tab = 1
        self.tab = None
        self.pane = None
        self.session = None
        self.pane = None
        self.tab = None
        self.sceneviewer = None
        self.networkeditor = None
        self.project_path = hou.hipFile.path()
        self.network_path = None
        self.tab_type = None
        self.update_objects()
        return

    def start(self):
        hou.ui.addEventLoopCallback(self.listener)

    def stop(self):
        hou.ui.removeEventLoopCallback(self.listener)

    def update_objects(self):
        self.tab = hou.ui.paneTabUnderCursor()
        self.pane = hou.ui.paneUnderCursor()

        self.session = Session()
        self.pane = Pane(hou.ui.paneUnderCursor())
        self.tab = Tab(self.tab)

        if self.tab != None:

            if self.tab.hasNetworkControls():
                self.network_path = self.tab.path()
            self.tab_type = self.tab.type()

            if self.tab.type() == "SceneViewer:"
                self.sceneviewer = SceneViewer(self.tab)
            else:
                self.sceneviewer = None

            if self.tab.type() == "NetworkEditor":
                self.networkeditor = NetworkEditor(self.tab)
            else:
                self.networkeditor = None

    def listener(self):
        tab = hou.ui.paneTabUnderCursor()
        if tab == None:
            hou.session.tab = None
        elif tab != hou.session.tab:
            print(tab)
            self.update_objects()

    def lists(self):
        # Arrays for navigating pane tabs
        self.tab_types = (
            hou.paneTabType.ApexEditor,
            hou.paneTabType.CompositorViewer,
            hou.paneTabType.DetailsView,
            hou.paneTabType.NetworkEditor,
            hou.paneTabType.Parm,
            hou.paneTabType.PythonPanel,
            hou.paneTabType.PythonShell,
            hou.paneTabType.SceneViewer,
            hou.paneTabType.Textport
        )
        self.tab_type_names = (
            "ApexEditor",
            "CompositorViewer",
            "DetailsView",
            "NetworkEditor",
            "Parm",
            "PythonPanel",
            "PythonShell",
            "SceneViewer",
            "Textport"
        )
        self.tab_names = [tab.name() for tab in hou.session.session.tabs()]

        # Populate pane tab labels array
        self.tab_labels = []
        for tab in self.session.tabs():
            index = self.tab_types.index(tab.type())
            label = self.tab_type_names[index]
            self.tab_labels.append(label)

    def networkPath(self):
        return str(hou.session.tab.pwd())

    def projectPath(self):
        return hou.hipFile.name()
        # ct = self.project_path.count("/")
        # self.project_path = self.project_path.split("/", ct - 2)[-1]
