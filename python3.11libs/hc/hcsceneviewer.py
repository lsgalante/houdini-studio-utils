import hou, types
from .hcpathtab import HCPathTab
from .hcviewport import HCViewport

"""
Layout/viewport IDs

DoubleSide:        2 3

DoubleStack:       3
                   0

Quad:              2 3
                   1 0

QuadBottomSplit:     3
                   2 1 0

QuadLeftSplit:     2
                   1 3
                   0

TripleBottomSplit:   3
                   1   0

TripleLeftSplit:   2
                   0 3
                   1

Single:
setViewportLayout(layout, single=-1)
-1: current viewport (viewportmouse is/was over)
0: top-left quad viewport (default: Top)
1: top-right quad viewport (default: Perspective)
2: bottom-left quad viewport (default: Front)
3: bottom-right quad viewport (default: Right)
"""

class HCSceneViewer(HCPathTab):
    def __init__(self, tab):
        self.tab = tab

    """ Geometry """

    def allDisplaySets(self):
        displaySets = []
        for hc_viewport in self.allHCViewports():
            settings = hc_viewport.settings()
            displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
            displaySets.append(displaySet)
        return displaySets

    def toggleLightGeo(self):
        self.setShowLights(not self.showLights())

    def toggleBackface(self):
        visible = 0
        displaySets = self.allDisplaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimBackfaces():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimBackfaces(not visible)

    def togglePointMarkers(self):
        visible = 0
        displaySets = self.allDisplaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointMarkers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointMarkers(not visible)

    def togglePointNormals(self):
        visible = 0
        displaySets = self.allDisplaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointNormals():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointNormals(not visible)

    def togglePointNumbers(self):
        visible = 0
        displaySets = self.allDisplaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointNumbers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointNumbers(not visible)

    def togglePrimNormals(self):
        visible = 0
        displaySets = self.allDisplaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimNormals():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimNormals(not visible)

    def togglePrimNumbers(self):
        visible = 0
        displaySets = self.allDisplaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimNumbers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimNumbers(not visible)

    def toggleVectors(self):
        for hc_viewport in self.allHCViewports():
            settings = viewport.settings()
            scale = settings.vectorScale()
            if scale == 1:
                settings.setVectorScale(0)
            elif scale == 0:
                settings.setVectorScale(1)
            else:
                settings.setVectorScale(1)

    """ Grids """

    def referencePlane(self):
        return self.tab.referencePlane()

    def toggleGrid(self):
        reference_plane = self.referencePlane()
        reference_plane.setIsVisible(not reference_plane.isVisible())


    """ Layout """

    def layout(self):
        return self.tab.viewportLayout()

    def layouts(self):
        return (
            hou.geometryViewportLayout.DoubleSide,
            hou.geometryViewportLayout.DoubleStack,
            hou.geometryViewportLayout.Quad,
            hou.geometryViewportLayout.QuadBottomSplit,
            hou.geometryViewportLayout.QuadLeftSplit,
            hou.geometryViewportLayout.TripleBottomSplit,
            hou.geometryViewportLayout.TripleLeftSplit,
            hou.geometryViewportLayout.Single,
        )

    def layoutIndices(self):
        return (
            (2, 3),
            (3, 0),
            (2, 3, 1, 0),
            (3, 2, 1, 0),
            (2, 1, 0, 3),
            (3, 1, 0),
            (2, 3, 1),
            (3),
        )

    def nextLayout(self):
        layouts = self.layouts()
        layout = self.layout()
        index = layouts.index(layout)
        index = (index+1) % len(layouts)
        self.setLayout(layouts[index])
        return

    def setLayout(self, layout):
        layout_map = {
            "DoubleSide":        hou.geometryViewportLayout.DoubleSide,
            "DoubleStack":       hou.geometryViewportLayout.DoubleStack,
            "Quad":              hou.geometryViewportLayout.Quad,
            "QuadBottomSplit":   hou.geometryViewportLayout.QuadBottomSplit,
            "QuadLeftSplit":     hou.geometryViewportLayout.QuadLeftSplit,
            "Single":            hou.geometryViewportLayout.Single,
            "TripleBottomSplit": hou.geometryViewportLayout.TripleBottomSplit,
            "TripleLeftSplit":   hou.geometryViewportLayout.TripleLeftSplit
        }
        self.tab.setViewportLayout(layout_map[layout])


    """ UI """

    def isVisibleDisplayBar(self):
        return self.tab.isShowingDisplayOptionsBar()

    def isVisibleGroupList(self):
        return self.tab.isGroupListVisible()

    def isVisibleOperationBar(self):
        return self.tab.isShowingOperationBar()

    def isVisibleSelectionBar(self):
        return self.tab.isShowingSelectionBar()

    def showDisplayBar(self, value):
        self.tab.showDisplayOptionsBar(value)

    def showGroupList(self, value):
        self.tab.setGroupListVisible(value)

    def showOperationBar(self, value):
        self.tab.showOperationBar(value)

    def showSelectionBar(self, value):
        self.tab.showSelectionBar(value)

    def toggleDisplayBar(self):
        self.showDisplayBar(not self.isVisibleDisplayBar())

    def toggleGroupList(self):
        self.showGroupList(not self.isVisibleGroupList)

    def toggleOperationBar(self):
        self.showOperationBar(not self.isVisibleOperationBar())

    def toggleSelectionBar(self):
        self.showSelectionBar(not self.isVisibleSelectionBar())

    def toggleBars(self):
        state = self.tab.isShowingOperationBar() + self.tab.isShowingDisplayOptionsBar() + self.tab.isShowingSelectionBar()
        if state > 0:
            self.showOperationBar(0)
            self.showDisplayBar(0)
            self.showSelectionBar(0)
        else:
            self.showOperationBar(1)
            self.showDisplayBar(1)
            self.showSelectionBar(1)

    """ Utils """

    def type(self):
        return "HCSceneViewer"

    def keycam(self):
        """
        Contexts:
        Chop, ChopNet, Cop, Cop2, CopNet, Data, Director, Dop, Driver, Lop, Manager, Object, Shop, Sop, Top, TopNet, Vop, VopNet
        """
        context_map = {
            "Object": "Keycam obj context",
            "Sop": "Keycam sop context",
            "Lop": "Keycam lop context",
        }
        context = self.pwd().childCat()
        if context in context_map:
            self.tab.setCurrentState('keycam')
            hou.ui.setStatusMessage(context_map[context])
        else:
            hou.ui.setStatusMessage("No obj, sop or lop context", hou.severityType.Error)


    """ Viewports """

    def homeAllViewports(self):
        for hc_viewport in self.allHCViewports():
            hc_viewport.home()

    def currentHCViewport(self):
        return self.tab.curViewport()

    def allHCViewports(self):
        hc_viewports = []
        for viewport in self.tab.viewports():
            hc_viewports.append(HCViewport(viewport))
        return hc_viewports()

    def frameAllViewports(self):
        for hc_viewport in self.allHCViewports():
            cam = hc_viewport.camera()
            # Is camera node or default
            if not cam:
                viewport.frameAll()
            else:
                viewport.frameAll()
