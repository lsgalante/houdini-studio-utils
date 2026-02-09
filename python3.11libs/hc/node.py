from .geo import Geo
import hou

class Node:
    def __init__(self, hou_node):
        self.hou_node = hou_node


    """ Selection """

    def currentNode(self):
        return self.__class__(self.hou_node.currentNode())

    def deselectAll(self):
        for child in self.selectedChildren():
            child.setSelected(False)

    def selectAllChildren(self):
        for child in self.children():
            child.setSelected(True)

    def selectedChildren(self):
        hou_nodes = self.hou_node.selectedChildren()
        return [self.__class__(hou_node) for hou_node in hou_nodes]

    def setSelected(self, state):
        self.hou_node.setSelected(state)


    """ Visibility """

    def displayNode(self):
        display_node = self.hou_node.displayNode()
        if display_node:
            return self.__class__(display_node)
        else:
            return None

    def visibleNodes(self):
        stack = self.children()
        visible_nodes = []

        while stack:
            node = stack.pop()
            if node.hou_node.isSubNetwork():
                child_cat = node.childCat()
                if child_cat == 'Object' and node.hou_node.isDisplayFlagSet():
                    stack.extend(node.children())
                elif child_cat == 'Sop' and node.hou_node.isDisplayFlagSet():
                    display_node = node.displayNode()
                    if display_node:
                        visible_nodes.append(display_node)

        return visible_nodes


    """ Geometry """

    def geometry(self):
        return self.hou_node.geometry()

    def hou_geo(self):
        geo = hou.Geometry()
        for node in self.visibleNodes():
            geo.merge(node.geometry())
        return geo


    """ Children """

    def childCat(self):
        """ Possibilities: Object, Sop, Lop """
        return self.hou_node.childTypeCategory().name()

    def children(self):
        hou_nodes = self.hou_node.children()
        return [self.__class__(hou_node) for hou_node in hou_nodes]

    def netPos(self):
        """ net editor xy position """
        return self.hou_node.position()


    """ Network """

    def position(self):
        return self.hou_node.position()

    def setColor(self, color):
        self.hou_node.setColor(color)

    def setPosition(self, pos):
        self.hou_node.setPosition(pos)

    def setUserData(self, a, b):
        self.hou_node.setUserData(a, b)

