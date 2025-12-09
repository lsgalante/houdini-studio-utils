import hou
import importlib
import ramp_color_presets
import ramp_color_schemes

def add_vis_callback(kwargs):
	node = kwargs['node']
	group = node.parmTemplateGroup()

	vis_index = 0
	for parm in group.entries():
		if parm.type() == hou.parmTemplateType.Folder:
			vis_index += 1

	enable_template = hou.ToggleParmTemplate(
		name='enable_' + str(vis_index),
		label="Enable",
		default_value=True,
		script_callback='hou.phm().enable_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python,
		join_with_next=True)

	update_folder_name_template = hou.ButtonParmTemplate(
		name='update_folder_name_' + str(vis_index),
		label="Update Folder Name",
		script_callback='hou.phm().update_folder_name_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)

	attr_template = hou.StringParmTemplate(
		name='attr_' + str(vis_index),
		label="Attribute",
		num_components=1,
		menu_items=('mag', 'mag2', 'mag3', 'dir', 'dir2', 'dir3'),
		menu_labels=("mag", "mag2", "mag3", "dir", "dir2", "dir3"),
		menu_type=hou.menuType.StringReplace,
		script_callback='hou.phm().attr_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)

	type_template = hou.MenuParmTemplate(
		name='type_' + str(vis_index),
		label="Type",
		menu_items=('color', 'marker'),
		menu_labels=("Color", "Marker"),
		script_callback='hou.phm().type_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)

	coloring_template = hou.MenuParmTemplate(
		name='coloring_' + str(vis_index),
		label="Coloring",
		menu_items=('fixed', 'vec_val', 'vec_dir', 'attr'),
		menu_labels=("Fixed Color", "Vector Values", "Vector Directions", "Attribute"),
		script_callback='hou.phm().coloring_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)
	coloring_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + str(vis_index) + ' != marker }')

	coloring_attr_template = hou.StringParmTemplate(
		name='coloring_attr_' + str(vis_index),
		label="Coloring Attribute",
		num_components=1,
		menu_items=('mag', 'mag2', 'mag3', 'dir', 'dir2', 'dir3'),
		menu_labels=("mag", "mag2", "mag3", "dir", "dir2", "dir3"),
		menu_type=hou.menuType.StringReplace,
		script_callback='hou.phm().coloring_attr_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)
	coloring_attr_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + str(vis_index) + ' != marker } { coloring_' + str(vis_index) + ' != attr }')

	sep1_template = hou.SeparatorParmTemplate(
		name='sep1_' + str(vis_index))

	preset_template = hou.MenuParmTemplate(
		name='preset_' + str(vis_index),
		label="Preset",
		menu_items=(),
		menu_labels=(),
		item_generator_script='hou.phm().generate_preset_menu()',
		script_callback='hou.phm().preset_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python,
		join_with_next=True)
	preset_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + str(vis_index) + ' == marker coloring_' + str(vis_index) + ' == fixed }')

	del_preset_template = hou.ButtonParmTemplate(
		name='del_preset_' + str(vis_index),
		label="Delete",
		script_callback='hou.phm().del_preset_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)
	del_preset_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + str(vis_index) + ' == marker coloring_' + str(vis_index) + ' == fixed }')

	interpol_template = hou.MenuParmTemplate(
		name='interpol_' + str(vis_index),
		label="Interpolation",
		menu_items=('Constant', 'Linear', 'CatmullRom', 'MonotoneCubic', 'Bezier', 'BSpline', 'Hermite'),
		menu_labels=("Constant", "Linear", "Catmull-Rom", "Monotone-Cubic", "Bezier", "B-Spline", "Hermite"),
		default_value=3,
		script_callback='hou.phm().interpol_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)
	interpol_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + str(vis_index) + ' == marker coloring_' + str(vis_index) + ' == fixed }')
	
	ramp_template = hou.RampParmTemplate(
		name='ramp_' + str(vis_index),
		label=" ",
		ramp_parm_type=hou.rampParmType.Color,
		show_controls=False,
		script_callback='hou.phm().ramp_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)
	ramp_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + str(vis_index) + ' == marker coloring_' + str(vis_index) + ' == fixed }')
	
	color_template = hou.FloatParmTemplate(
		name='color_' + str(vis_index),
		label="Color",
		num_components=3,
		naming_scheme=hou.parmNamingScheme.RGBA,
		look=hou.parmLook.ColorSquare,
		script_callback='hou.phm().color_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)
	color_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + str(vis_index) + ' != marker } { coloring_' + str(vis_index) + ' != fixed }')
	
	length_template = hou.FloatParmTemplate(
		name='length_' + str(vis_index),
		label="Length",
		num_components=1,
		max=1.0,
		script_callback='hou.phm().length_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python)
	length_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + str(vis_index) + ' != marker }')
	
	sep2_template = hou.SeparatorParmTemplate(
		name='sep2_' + str(vis_index))
	
	del_vis_template = hou.ButtonParmTemplate(
		name='del_vis_' + str(vis_index),
		label="Delete Visualizer",
		script_callback='hou.phm().del_vis_callback(kwargs)',
		script_callback_language=hou.scriptLanguage.Python,
		join_with_next=True)
	
	folder_template = hou.FolderParmTemplate(
		name='folder_' + str(vis_index),
		label="Vis " + str(vis_index),
		parm_templates=([
			enable_template,
			update_folder_name_template,
			attr_template,
			type_template,
			coloring_template,
			coloring_attr_template,
			sep1_template,
			preset_template,
			del_preset_template,
			interpol_template,
			ramp_template,
			color_template,
			length_template,
			sep2_template,
			del_vis_template]),
		folder_type=hou.folderType.Tabs)

	group.append(folder_template)
	node.setParmTemplateGroup(group)

	vis = hou.viewportVisualizers.createVisualizer(
		hou.viewportVisualizers.type('vis_color'),
		hou.viewportVisualizerCategory.Node,
		hou.node('./vis'))
	update(kwargs)

def enable_callback(kwargs):
	vis_index = kwargs['parm_name'].removeprefix('enable_')
	vis = get_vis(vis_index)
	val = kwargs['parm'].evalAsInt()
	if val == 1:
		vis.setIsActive(True)
	if val == 0:
		vis.setIsActive(False)

def attr_callback(kwargs):
	vis_index = kwargs['parm_name'].removeprefix('attr_')
	vis = get_vis(vis_index)
	val = kwargs['parm'].evalAsString()
	vis.setParm('attrib', val)

def type_callback(kwargs):
	vis_index = kwargs['parm_name'].removeprefix('type_')
	vis = get_vis(vis_index)
	val = kwargs['parm'].evalAsInt()
	if val == 0:
		vis.setType(hou.viewportVisualizers.types()[1])
		vis.setParm('colortype', 1)
		vis.setParm('rangespec', 1)
		vis.setParm('clamptype', 1)
	if val == 1:
		vis.setType(hou.viewportVisualizers.types()[0])
		vis.setParm('style', 4)
		kwargs['node'].parm('coloring_' + str(vis_index)).pressButton()

def coloring_callback(kwargs):
	if kwargs['parm'].isHidden() == False:
		vis_index = kwargs['parm_name'].removeprefix('coloring_')
		vis = get_vis(vis_index)
		val = kwargs['parm'].evalAsInt()
		vis.setParm('vectorcoloring', val)
		if val == 0:
			kwargs['node'].parm('color_' + str(vis_index) + 'r').pressButton()
		if val != 0:
			vis.setParm('ramptype', 6)
			vis.setParm('rangespec', 0)
		if val == 3:
			kwargs['node'].parm('coloring_attr_' + str(vis_index)).pressButton()

def preset_callback(kwargs):
	if kwargs['parm'].isHidden() == False:
		vis_index = kwargs['parm_name'].removeprefix('preset_')
		val = kwargs['parm'].evalAsString()
		ramp_parm = kwargs['node'].parm('ramp_' + str(vis_index))
		
		if val == 'new':
			new_preset(parm, ramp_parm)
			kwargs['parm'].set(0)
		if val == '_separator_':
			return
		if val != 'new' and val != '_separator_':
			vis = get_vis(vis_index)
			ramp_val = getattr(ramp_color_schemes, val)
			ramp_parm.set(ramp_val)
			vis.setParm('colorramp', ramp_val)

def del_preset_callback(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	vis_index = kwargs['parm_name'].removeprefix('del_preset_')
	preset_parm = kwargs['node'].parm('preset_' + str(vis_index))
	preset_val = preset_parm.evalAsString()

	menu = ramp_color_presets.menu
	menu.remove(preset_val)
	menu.remove(preset_val)

	presets_file = open('C:/Users/lucas/OneDrive/Git/morphogen/scripts/ramp_color_presets.py', 'w')
	presets_file.write('menu=' + str(menu))
	presets_file.close()
	preset_parm.set(0)

	scheme = getattr(ramp_color_schemes, preset_val)
	scheme = new_scheme(preset_val, scheme)

	path = 'C:/Users/lucas/OneDrive/Git/morphogen/scripts/ramp_color_schemes.py'

	schemes_file = open(path, 'r').read()
	ramp_color_schemes = schemes_file.replace(scheme, '')
	schemes_file.close()

	schemes_file = open(path, 'w')
	schemes_file.write(ramp_color_schemes)
	schemes_file.close()

	importlib.reload(ramp_color_presets)
	importlib.reload(ramp_color_schemes)

def interpol_callback(kwargs):
	if kwargs['parm'].isHidden() == False:
		vis_index = kwargs['parm_name'].removeprefix('interpol_')
		vis = get_vis(vis_index)
		val = kwargs['parm'].evalAsString()

		ramp_parm = kwargs['node'].parm('ramp_' + str(vis_index))
		ramp_val = ramp_parm.evalAsRamp()
		
		basis = ramp_val.basis()
		keys = ramp_val.keys()
		values = ramp_val.values()
		
		new_basis = []
		for x in basis:
				new_basis.append(eval('hou.rampBasis.' + val))

		new_ramp = hou.Ramp(new_basis, keys, values)
		ramp_parm.set(new_ramp)
		
		vis.setParm('colorramp', new_ramp)

def ramp_callback(kwargs):
	if kwargs['parm'].isHidden() == False:
		vis_index = kwargs['parm_name'].removeprefix('ramp_')
		vis = get_vis(vis_index)
		val = kwargs['parm'].evalAsRamp()

		vis.setParm('colorramp', val)

def color_callback(kwargs):
	vis_index = kwargs['parm_name'].removeprefix('color_')
	vis_index = str(vis_index).removesuffix('r')
	vis = get_vis(vis_index)

	if kwargs['node'].parm('color_' + vis_index + 'r').isHidden() == False:
		colorr = kwargs['node'].parm('color_' + vis_index + 'r').eval()
		colorg = kwargs['node'].parm('color_' + vis_index + 'g').eval()
		colorb = kwargs['node'].parm('color_' + vis_index + 'b').eval()

		vis.setParm('markercolorr', colorr)
		vis.setParm('markercolorg', colorg)
		vis.setParm('markercolorb', colorb)

def coloring_attr_callback(kwargs):
	if kwargs['parm'].isHidden() == False:
		vis_index = kwargs['parm_name'].removeprefix('coloring_attr_')
		vis = get_vis(vis_index)
		val = kwargs['node'].parm('coloring_attr_' + str(vis_index)).evalAsString()

		vis.setParm('colorattrib', val)

def length_callback(kwargs):
	if kwargs['parm'].isHidden() == False:
		vis_index = kwargs['parm_name'].removeprefix('length_')
		vis = get_vis(vis_index)
		val = kwargs['parm'].evalAsFloat()
		vis.setParm('lengthscale', val)

def del_vis_callback(kwargs):
	vis_index = kwargs['parm_name'].removeprefix('del_vis_')
	vis = get_vis(vis_index)
	vis.destroy()

	group = kwargs['node'].parmTemplateGroup()
	entries = list(group.entries())
	entry_index = -1
	folder_name = 'folder_0'
	if vis_index != '0':
		folder_name = 'folder_0_' + str(vis_index)
	for entry in entries:
		entry_index += 1
		if entry.name() == folder_name:
			entries.pop(entry_index)

	vis_index = -1
	for entry in entries:
		if entry.type() == hou.parmTemplateType.Folder:
			vis_index += 1
			if vis_index == 0:
				entry.setName('folder_0')
			else:
				entry.setName('folder_0_' + str(vis_index))
			parm_templates = entry.parmTemplates()
			index = -1
			for parm_template in parm_templates:
				index += 1
				if parm_template.label() == 'Enable':
					new_name = 'enable_' + str(vis_index)
					parm_template.setName(new_name)

				if parm_template.label() == 'Update Folder Name':
					parm_template.setName('update_folder_name_' + str(vis_index))
					
				if parm_template.label() == 'Attribute':
					parm_template.setName('attr_' + str(vis_index))
				
				if parm_template.label() == 'Type':
					parm_template.setName('type_' + str(vis_index))
				
				if parm_template.label() == 'Coloring':
					parm_template.setName('coloring_' + str(vis_index))
					parm_template.setConditional(
						hou.parmCondType.HideWhen,
						'{ type_' + str(vis_index) + ' != marker }')
				
				if parm_template.label() == 'Coloring Attribute':
					parm_template.setName('coloring_attr_' + str(vis_index))
					parm_template.setConditional(
						hou.parmCondType.HideWhen,
						'{ type_' + str(vis_index) + ' != marker } { coloring_' + str(vis_index) + ' != attr }')
				
				if parm_template.name().find('sep1') >= 0:
					parm_template.setName('sep1_' + str(vis_index))
				
				if parm_template.label() == 'Preset':
					parm_template.setName('preset_' + str(vis_index))
					parm_template.setConditional(
						hou.parmCondType.HideWhen,
						'{ type_' + str('vis_index') + ' == marker coloring_' + str(vis_index) + ' == fixed }')
				
				if parm_template.label() == 'Delete':
					parm_template.setName('del_preset_' + str(vis_index))
					parm_template.setConditional(
						hou.parmCondType.HideWhen,
						'{ type_' + str('vis_index') + ' == marker coloring_' + str(vis_index) + ' == fixed }')
				
				if parm_template.label() == 'Interpolation':
					parm_template.setName('interpol_' + str(vis_index))
					parm_template.setConditional(
						hou.parmCondType.HideWhen,
						'{ type_' + str(vis_index) + ' == marker coloring_' + str(vis_index) + ' == fixed }')
				
				if parm_template.type() == hou.parmTemplateType.Ramp:
					parm_template.setName('ramp_' + str(vis_index))
					parm_template.setConditional(
						hou.parmCondType.HideWhen,
						'{ type_' + str(vis_index) + ' == marker coloring_' + str(vis_index) + ' == fixed }')

				if parm_template.label() == 'Color':
					parm_template.setName('color_' + str(vis_index))
					parm_template.setConditional(
						hou.parmCondType.HideWhen,
						'{ type_' + str(vis_index) + ' != marker } { coloring_' + str(vis_index) + ' != fixed }')
				
				if parm_template.label() == 'Length':
					parm_template.setName('length_' + str(vis_index))
					parm_template.setConditional(
						hou.parmCondType.HideWhen,
						'{ type_' + str(vis_index) + ' != marker }')
				
				if parm_template.name().find('sep2') >= 0:
					parm_template.setName('sep2_' + str(vis_index))

				if parm_template.label() == 'Delete Visualizer':
					parm_template.setName('del_vis_' + str(vis_index))

			entry.setParmTemplates(parm_templates)

	# print(entries)

	kwargs['node'].setParmTemplateGroup(hou.ParmTemplateGroup(entries))
	
	update(kwargs)

def update(kwargs):	
	visualizers = hou.viewportVisualizers.visualizers(hou.viewportVisualizerCategory.Node, hou.node('./vis'))
	vis_index = 0
	for visualizer in visualizers:
		vis_index = str(vis_index)
		kwargs['node'].parm('enable_' + vis_index).pressButton()
		kwargs['node'].parm('type_' + vis_index).pressButton()
		kwargs['node'].parm('attr_' + vis_index).pressButton()
		kwargs['node'].parm('preset_' + vis_index).pressButton()
		kwargs['node'].parm('coloring_' + vis_index).pressButton()
		kwargs['node'].parm('coloring_attr_' + vis_index).pressButton()
		kwargs['node'].parm('ramp_' + vis_index).pressButton()
		kwargs['node'].parm('color_' + vis_index + 'r').pressButton()
		kwargs['node'].parm('length_' + vis_index).pressButton()
		vis_index = int(vis_index)
		vis_index += 1

def update_folder_name_callback(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']
	vis_index = kwargs['parm_name'].removeprefix('update_folder_name_')
	attr_parm = node.parm('attr_' + str(vis_index))
	attr_val = attr_parm.evalAsString()

	group = node.parmTemplateGroup()
	
	entries = group.entries()
	
	folder_template = entries[int(vis_index) + 2]
	new_folder_template = folder_template.clone()

	if attr_val == "":
		new_folder_template.setLabel("Vis " + vis_index)

	else:
		new_folder_template.setLabel(attr_val)

	group.replace(folder_template, new_folder_template)

	node.setParmTemplateGroup(group)

def get_vis(vis_index):
	vistup = hou.viewportVisualizers.visualizers(
		hou.viewportVisualizerCategory.Node,
		hou.node('./vis'))
	vis = vistup[int(vis_index)]
	return(vis)

def generate_preset_menu():
	importlib.reload(ramp_color_presets)
	menu = ramp_color_presets.menu
	return(menu)

def new_preset(preset_parm, ramp_parm):
	new_name = hou.ui.readInput("New Preset", buttons = ("Add", "Cancel"))
	if new_name[0] == 0:
		menu = ramp_color_presets.menu
		menu.insert(0, new_name[1])
		menu.insert(0, new_name[1])

		ramp_val = ramp_parm.evalAsRamp()
		new_scheme = new_scheme(new_name[1], ramp_val)
		
		menu_file = open('C:/Users/lucas/OneDrive/Git/morphogen/scripts/ramp_color_presets.py', 'w')
		menu_file.write('menu=' + str(menu))
		menu_file.close()

		scheme_file = open('C:/Users/lucas/OneDrive/Git/morphogen/scripts/ramp_color_schemes.py', 'a')
		scheme_file.write(new_scheme)
		scheme_file.close()

		importlib.reload(ramp_color_presets)
		importlib.reload(ramp_color_schemes)
		preset_parm.set(0)

def new_scheme(preset_val, ramp_val):
	basis = ramp_val.basis()
	basis = tuple('hou.' + str(x) for x in basis)
	basis = str(basis).replace("'", "")

	keys = ramp_val.keys()
	keys = tuple(round(x, 4) for x in keys)

	values = ramp_val.values()
	values = tuple(tuple(round(x2, 4) for x2 in x) for x in values)

	scheme = '\n' + preset_val + '=' + 'hou.Ramp(' + str(basis) + ',' + str(keys) + ',' + str(values) + ')\n'

	return(scheme)