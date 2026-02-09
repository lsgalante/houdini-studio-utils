import hou


class Viewport():
    def __init__(self, hou_viewport):
        self.hou_viewport = hou_viewport
        return

    def visualizers(self):
        category = hou.viewportVisualizerCategory.Scene
        vis_arr = hou.viewportVisualizers.visualizers(category)
        return vis_arr

    def setType(self, type):
        self.hou_viewport.changeType(type)
