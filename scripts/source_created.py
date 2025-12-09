import hou

network = hou.node(".")
node = kwargs['node']

solver = network.createNode("morphosolver")

solver.setInput(0, node, 0)