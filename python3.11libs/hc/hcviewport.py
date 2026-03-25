import hou

class HCViewport():
    def __init__(self, viewport):
        self.viewport = viewport

    def displaySet(self):
        settings = self.viewport.settings()
        display_set = settings.displaySet(hou.displaySetType.DisplayModel)
        return displaySet

    def visualizers(self):
        category = hou.viewportVisualizerCategory.Scene
        vis_arr = hou.viewportVisualizers.visualizers(category)
        return vis_arr

    def setType(self, type):
        self.viewport.changeType(type)
