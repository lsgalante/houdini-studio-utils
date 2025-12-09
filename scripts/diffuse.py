import hou

def gainlosslink(kwargs):

    node = kwargs["node"]

    gain = node.parm("gain").eval()

    loss = node.parm("loss")

    loss.set(gain)

def avg(node):
    
    valnode = hou.node('./valnode')
    geo = valnode.geometry()
    avg = geo.attribValue('avg')
    
    thisnode = hou.pwd()
    thisnode.parm('diffusegoal').set(avg)
    
def min(node):
    
    valnode = hou.node('./valnode')
    geo = valnode.geometry()
    min = geo.attribValue('min')
    
    thisnode = hou.pwd()
    thisnode.parm('diffusegoal').set(min)
    
def max(node):
    
    valnode = hou.node('./valnode')
    geo = valnode.geometry()
    max = geo.attribValue('max')
    
    thisnode = hou.pwd()
    thisnode.parm('diffusegoal').set(max)