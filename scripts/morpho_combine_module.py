def update_description(kwargs):
	node = kwargs['node']
	n_inputs = len(node.inputs())
	desc = ''
	for n in range(n_inputs):
		attr_parm = node.parm('attrs' + str(n))
		if n != 0:
			desc += '\n'
		attr_str = attr_parm.evalAsString()
		desc += str(n) + ': ' + attr_str
	desc_parm = node.parm('desc')
	desc_parm.set(desc)