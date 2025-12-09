def update_description(kwargs):
	node = kwargs['node']
	n_ops_parm = node.parm('n_ops')
	n_ops = n_ops_parm.evalAsInt()
	desc = ''
	for n_op in range(n_ops):
		attr = node.parm('attr' + str(n_op)).evalAsString()
		op = node.parm('op' + str(n_op)).evalAsString()
		if op == 'set':
			desc = attr + ' '

		if op == 'add':
			desc += '+ ' + attr + ' '

		if op == 'sub':
			desc += '- ' + attr + ' '

		if op == 'multi':
			desc += '* ' + attr + ' '

		if op == 'raise':
			desc += '^ ' + attr + ' '

		if op == 'min':
			desc = 'min(' + attr + ') '

		if op == 'max':
			desc = 'max(' + attr + ') '
			
		if op == 'avg':
			desc = 'avg(' + attr + ') '

	result = node.parm('result').evalAsString()
	desc += '= ' + result
	desc_parm = node.parm('desc')
	desc_parm.set(desc)

def op_menu(kwargs):
	menu = []

	node = kwargs['node']
	mp_index = kwargs['script_multiparm_index']

	new_type_parm = node.parm("type" + str(mp_index))
	new_type = new_type_parm.evalAsString()

	op_parm = node.parm("op" + str(mp_index))
	op = op_parm.evalAsString()

	current_type = "x"
	if mp_index > 0:
		current_type_parm = node.parm("type" + str(mp_index - 1))
		current_type = current_type_parm.evalAsString()

	if mp_index == 0:
		menu = ["set", "Set"]

	if new_type == "float" and current_type == "float":
		menu = ["set", "Set", "add", "Add", "sub", "Subtract", "multi", "Multiply", "raise", "Raise", "min", "Min", "max", "Max", "avg", "Average"]

	if new_type == "float" and current_type == "vec":
		menu = ["set", "Set", "multi", "Multiply", "raise", "Raise"]

	if new_type == "vec" and current_type == "float":
		menu = ["set", "Set", "multi", "Multiply"]

	if new_type == "vec" and current_type == "vec":
		menu = ["set", "Set", "add", "Add", "sub", "Subtract", "multi", "Multiply", "min", "Min", "max", "Max", "avg", "Average"]

	return menu