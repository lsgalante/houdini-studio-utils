import hou
from .geo  import Geo
from .node import Node
from .tab  import Tab

class PathTab(Tab):
    def __init__(self, hou_tab):
        self.hou_tab = hou_tab

    def geo(self):
        return Geo(self.hou_geo())

    def hou_geo(self):
        visible_nodes = self.pwd().visibleNodes()
        geo = hou.Geometry()

        for node in visible_nodes:
            geo.merge(node.geometry())

        return geo

    def path(self):
        return self.pwd().path()

    def pwd(self):
        return Node(self.hou_tab.pwd())
