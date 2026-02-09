import hou, types
from .pathtab import PathTab

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

class SceneViewer(PathTab):
    def __init__(self, hou_tab):
        self.hou_tab = hou_tab


    """ Geometry """

    def displaySets(self):
        displaySets = []
        for viewport in self.viewports():
            settings = viewport.settings()
            displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
            displaySets.append(displaySet)
        return(displaySets)

    def toggleLightGeo(self):
        self.setShowLights(not self.showLights())

    def toggleBackface(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimBackfaces():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimBackfaces(not visible)

    def togglePointMarkers(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointMarkers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointMarkers(not visible)

    def togglePointNormals(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointNormals():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointNormals(not visible)

    def togglePointNumbers(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointNumbers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointNumbers(not visible)

    def togglePrimNormals(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimNormals():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimNormals(not visible)

    def togglePrimNumbers(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimNumbers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimNumbers(not visible)

    def toggleVectors(self):
        for viewport in self.viewports():
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
        return self.hou_tab.referencePlane()

    def toggleGrid(self):
        refplane = self.referencePlane()
        refplane.setIsVisible(not refplane.isVisible())


    """ Layout """

    def layout(self):
        return self.hou_tab.viewportLayout()

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
        self.hou_tab.setViewportLayout(layout_map[layout])


    """ UI """

    def isVisibleDisplayBar(self):
        return self.hou_tab.isShowingDisplayOptionsBar()

    def isVisibleGroupList(self):
        return self.hou_tab.isGroupListVisible()

    def isVisibleOperationBar(self):
        return self.hou_tab.isShowingOperationBar()

    def isVisibleSelectionBar(self):
        return self.hou_tab.isShowingSelectionBar()

    def showDisplayBar(self, value):
        self.hou_tab.showDisplayOptionsBar(value)

    def showGroupList(self, value):
        self.hou_tab.setGroupListVisible(value)

    def showOperationBar(self, value):
        self.hou_tab.showOperationBar(value)

    def showSelectionBar(self, value):
        self.hou_tab.showSelectionBar(value)

    def toggleDisplayBar(self):
        self.showDisplayBar(not self.isVisibleDisplayBar())

    def toggleGroupList(self):
        self.showGroupList(not self.isVisibleGroupList)

    def toggleOperationBar(self):
        self.showOperationBar(not self.isVisibleOperationBar())

    def toggleSelectionBar(self):
        self.showSelectionBar(not self.isVisibleSelectionBar())

    def toggleBars(self):
        state = self.hou_tab.isShowingOperationBar() + self.hou_tab.isShowingDisplayOptionsBar() + self.hou_tab.isShowingSelectionBar()
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
        return "SceneViewer"

    def keycam(self):
        """
        Contexts:
        Chop, ChopNet, Cop, Cop2, CopNet, Data, Director, Dop, Driver, Lop, Manager, Object, Shop, Sop, Top, TopNet, Vop, VopNet
        """
        context_map = {
            "Object": "Entered keycam in an obj context",
            "Sop": "Entered keycam in a sop context",
            "Lop": "Entered keycam in a lop context",
        }
        context = self.pwd().childCat()
        if context in context_map:
            self.hou_tab.setCurrentState('keycam')
            hou.ui.setStatusMessage(context_map[context])
        else:
            hou.ui.setStatusMessage("No obj, sop or lop context", hou.severityType.Error)


    """ Viewports """

    def homeAllViewports(self):
        for viewport in self.viewports():
            viewport.home()

    def currentViewport(self):
        return self.hou_tab.curViewport()

    def allViewports(self):
        return self.hou_tab.viewports()

    def frame(self):
        for viewport in self.allViewports():
            cam = viewport.camera()
            # Is camera node or default
            if not cam:
                viewport.frameAll()
            else:
                viewport.frameAll()
