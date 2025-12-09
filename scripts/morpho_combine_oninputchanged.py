node = kwargs['node']

inputs = node.inputs()
n_inputs = len(inputs)

group = hou.ParmTemplateGroup(())
group.append(node.parm('iterations').parmTemplate())
group.append(node.parm('desc').parmTemplate())

for i in range(n_inputs):
	string_template = hou.StringParmTemplate(
		name='attrs' + str(i),
		label='Input ' + str(i) + ' Attributes',
		num_components=1,
		default_value=(''),
		item_generator_script="kwargs['node'].generateInputAttribMenu(" + str(i) + ", hou.attribType.Point)",
		menu_type=hou.menuType.StringToggle,
		script_callback='hou.phm().update_description(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)
	group.append(string_template)

node.setParmTemplateGroup(group)

iterations_parm = node.parm('iterations')
iterations_parm.set(n_inputs)

#############

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