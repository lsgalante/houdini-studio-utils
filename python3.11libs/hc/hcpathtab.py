import hou
from .hcgeo  import HCGeo
from .hcnode import HCNode
from .hctab  import HCTab

class HCPathTab(HCTab):
    def __init__(self, tab):
        self.tab = tab

    def hcGeo(self):
        return HCGeo(self.geo())

    def geo(self):
        visible_nodes = self.pwd().visibleNodes()
        geo = hou.Geometry()
        for node in visible_nodes:
            geo.merge(node.geometry())
        return geo

    def path(self):
        return self.pwd().path()

    def pwd(self):
        return Node(self.tab.pwd())
