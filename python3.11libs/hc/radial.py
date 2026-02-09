import hou

#
# PaneTab object is retrieved by calling kwargs["pane"]
#

class Radial:
    def __init__(self):
        return

    def createItem(label="label", pos=0, submenu=False, script="script"):
        item = hou.ui.createRadialItem(submenu=submenu)
        item.setLabel(label)
        item.setScript(script)
        hou.ui.injectRadialItem(pos, item)

    #
    # Scene Viewer
    #

    def sceneViewerMain(**kwargs):
        menu = hou.ui.createRadialMenu("hc_radial_sceneviewer_main", "HC Radial Scene Viewer Main")
        createItem(
            pos=0,
            label="UI",
            submenu=True, script="from hc import Radial; Radial.sceneViewerUI()"
        )
        createItem(
            pos=7,
            label="Operation bar",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).toggleOperationBar()"
        )
        createItem(
            pos=6,
            label="Display bar",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).toggleDisplayOptionsToolbar()"
        )
        createItem(
            pos=5,
            label="Selection bar",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).toggleSelectionBar()"
        )
        createItem(
            pos=4,
            label="Keycam",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).keycam()"
        )
        return menu

    def sceneViewerLayout(**kwargs):
        menu = hou.ui.createRadialMenu("hc_radial_sceneviewer_layout", "HC Radial - Scene Viewer Layout")
        createItem(
            pos=0,
            label="DoubleSide",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).setLayout('DoubleSide')"
        )
        createItem(
            pos=1,
            label="DoubleStack",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).setLayout('DoubleStack')"
        )
        createItem(
            pos=2,
            label="Quad",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).setLayout('Quad')"
        )
        createItem(
            pos=3,
            label="QuadBottomSplit",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).setLayout('QuadBottomSplit')"
        )
        createItem(
            pos=4,
            label="QuadLeftSplit",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).setLayout('QuadLeftSplit')"
        )
        createItem(
            pos=5,
            label="Single",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).setLayout('Single')"
        )
        createItem(
            pos=6,
            label="TripleBottomSplit",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).setLayout('TripleBottomSplit')"
        )
        createItem(
            pos=7,
            label="TripleLeftSplit",
            script="from hc import SceneViewer; SceneViewer(kwargs['pane']).setLayout('TripleLeftSplit')"
        )
        return menu

    def sceneViewerUI(**kwargs):
        menu = hou.ui.createRadialMenu("hc_radial_sceneviewer_ui", "HC Radial - Scene Viewer UI")
        createItem(
            pos=0,
            label="Tabs",
            script="from hc import Tab; Tab(kwargs['pane']).pane().toggleTabs()"
        )
        createItem(
            pos=7,
            label="Path",
            script="from hc import Tab; Tab(kwargs['pane']).toggleNetworkControls()"
        )
        createItem(
            pos=6,
            label="Maximize",
            script="from hc import Tab; Tab(kwargs['pane']).pane().toggleMaximize()"
        )
        createItem(
            pos=5,
            label="Stowbars",
            script="from hc import Session; Session().toggleStowbars()"
        )
        createItem(
            pos=4,
            label="All tabs",
            script="from hc import Session; Session().toggleTabs()"
        )
        createItem(
            pos=3,
            label="All paths",
            script="from hc import Session; Session().toggleNetworkControls()"
        )
        createItem(
            pos=2,
            label="Layout",
            submenu=True, script="from hc import radialutils; radialutils.viewerRadialLayout()"
        )
        return menu


    def networkEditorMain(**kwargs):
        menu = hou.ui.createRadialMenu("hc_radial_networkeditor", "HC Radial - Network Editor")
        createItem(
            pos=0,
            submenu=True,
            label="UI",
            script="from hc import Radial; Radial.networkEditorUI()"
        )
        createItem(
            pos=7,
            label="Menu",
            script="from hc import NetworkEditor; NetworkEditor(kwargs['pane']).toggleMenu()"
        )
        createItem(
            pos=6,
            label="Frame all",
            script="from hc import NetworkEditor; NetworkEditor(kwargs['pane']).frameAll()"
        )
        return menu

    def networkEditorUI(**kwargs):
        menu = hou.ui.createRadialMenu("hc_radial_networkeditor", "HC Radial - Network Editor")
        createItem(
            pos=0,
            label="Tabs",
            script="from hc import Tab; Tab(kwargs['pane']).pane().toggleTabs()"
        )
        createItem(
            pos=7,
            label="Path",
            script="from hc import Tab; Tab(kwargs['pane']).toggleNetworkControls()"
        )
        createItem(
            pos=6,
            label="All tabs",
            script="from hc import Session; Session().toggleTabs()"
        )
        createItem(
            pos=5,
            label="All paths",
            script="from hc import Session; Session().toggleNetworkControls()"
        )
        createItem(
            pos=4,
            label="Stowbars",
            script="from hc import Session; Session().toggleStowbars()"
        )
        createItem(
            pos=3,
            label="Maximize",
            script="from hc import Tab; Tab(kwargs['pane']).pane().toggleMaximize()"
        )
        return menu
