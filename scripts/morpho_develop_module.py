def desc(kwargs):
	node = kwargs['node']
	dir_attr = node.parm('dir_attr').evalAsString()
	multi__attr = node.parm('multi_attr').evalAsString()
	desc_parm = node.parm('desc')
	desc = '@P += ' + dir_attr + ' * ' + multi__attr
	desc_parm.set(desc)