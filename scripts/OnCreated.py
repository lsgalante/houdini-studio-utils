import hou
from hc import Prefs
from hc import Node
# import from hc.NetworkEditor import snapToGrid

# Get the node that was just created
node = Node(kwargs['node'])

# Force the shape to your desired JSON name
# (e.g., "rect", "circle", or your custom "my_shape")
node.setUserData("nodeshape", "rect")
node.setColor(hou.Color(Prefs().node_color))
# snapToGrid(node)
