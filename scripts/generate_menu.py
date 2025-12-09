node = kwargs['node']
geometry = node.geometry()
pts = geometry.pointAttribs()
dets = geometry.globalAttribs()
menu = []
menu.append('pt_attrs')
menu.append('Point Attributes:')
for pt in pts:
	menu.append('pt-' + pt.name())
	menu.append(pt.name())
menu.append('_separator_')
menu.append('_separator_')
menu.append('det_attrs')
menu.append('Detail Attributes:')
for det in dets:
	menu.append('det-' + det.name())
	menu.append(det.name())
return(menu)