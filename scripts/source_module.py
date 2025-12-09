import hou
import importlib
import stain_menu
import stain_schemes

def addvis(kwargs):
	node = kwargs['node']
	group = node.parmTemplateGroup()
	top_folder = group.findFolder("Visualizers")

	vis_id = 0
	bottom_folders = top_folder.parmTemplates()
	for bottom_folder in bottom_folders:
		vis_id += 1

	vis_id = str(vis_id)

	enable_template = hou.ToggleParmTemplate(
		'enable_' + vis_id,
		label = "Enable Visualizer",
		default_value = True,
		script_callback = 'hou.phm().enable(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	attr_template = hou.StringParmTemplate(
		name = 'attr_' + vis_id,
		label = "Attribute",
		num_components = 1,
		menu_items = ('mag', 'mag2', 'mag3', 'dir', 'dir2', 'dir3'),
		menu_labels = ("mag", "mag2", "mag3", "dir", "dir2", "dir3"),
		menu_type = hou.menuType.StringReplace,
		script_callback = 'hou.phm().attr(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	type_template = hou.MenuParmTemplate(
		name = 'type_' + vis_id,
		label = "Type",
		menu_items = ('color', 'marker'),
		menu_labels = ("Color", "Marker"),
		script_callback = 'hou.phm().type(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	coloring_template = hou.MenuParmTemplate(
		name = 'coloring_' + vis_id,
		label = "Coloring",
		menu_items = ('fixed', 'val', 'dir', 'other'),
		menu_labels = ("Fixed Color", "Vector Values", "Vector Directions", "Other Attribute"),
		script_callback = 'hou.phm().coloring(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	coloring_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + vis_id + ' != marker }')

	otherattr_template = hou.StringParmTemplate(
		name = 'otherattr_' + vis_id,
		label = "Other Attribute",
		num_components = 1,
		menu_items = ('mag', 'mag2', 'mag3', 'dir', 'dir2', 'dir3'),
		menu_labels = ("mag", "mag2", "mag3", "dir", "dir2", "dir3"),
		menu_type = hou.menuType.StringReplace,
		script_callback = 'hou.phm().otherattr(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	otherattr_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + vis_id + ' != marker } { coloring_' + vis_id + ' != other }')

	sep1_template = hou.SeparatorParmTemplate(
		name = 'sep1_' + vis_id)

	preset_template = hou.MenuParmTemplate(
		name = 'preset_' + vis_id,
		label = "Preset",
		menu_items = (),
		menu_labels = (),
		item_generator_script = 'hou.phm().presetmenu()',
		script_callback = 'hou.phm().preset(kwargs)',
		script_callback_language = hou.scriptLanguage.Python,
		join_with_next = True)

	preset_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + vis_id + ' == marker coloring_' + vis_id + ' == fixed }')

	delpreset_template = hou.ButtonParmTemplate(
		name = 'delpreset_' + vis_id,
		label = "Delete Preset",
		script_callback = 'hou.phm().delpreset(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	delpreset_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + vis_id + ' == marker coloring_' + vis_id + ' == fixed }')

	interpol_template = hou.MenuParmTemplate(
		name = 'interpol_' + vis_id,
		label = "Interpolation",
		menu_items = ('Constant', 'Linear', 'CatmullRom', 'MonotoneCubic', 'Bezier', 'BSpline', 'Hermite'),
		menu_labels = ("Constant", "Linear", "Catmull-Rom", "Monotone-Cubic", "Bezier", "B-Spline", "Hermite"),
		default_value = 3,
		script_callback = 'hou.phm().interpol(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	interpol_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + vis_id + ' == marker coloring_' + vis_id + ' == fixed }')

	ramp_template = hou.RampParmTemplate(
		name = 'ramp_' + vis_id,
		label = "Color Ramp",
		ramp_parm_type = hou.rampParmType.Color,
		show_controls = False,
		script_callback = 'hou.phm().ramp(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	ramp_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + vis_id + ' == marker coloring_' + vis_id + ' == fixed }')

	color_template = hou.FloatParmTemplate(
		name = 'color_' + vis_id,
		label = "Color",
		num_components = 3,
		naming_scheme = hou.parmNamingScheme.RGBA,
		look = hou.parmLook.ColorSquare,
		script_callback = 'hou.phm().color(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	color_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + vis_id + ' != marker } { coloring_' + vis_id + ' != fixed }')

	length_template = hou.FloatParmTemplate(
		name = 'length_' + vis_id,
		label = "Length Scale",
		num_components = 1,
		max = 1.0,
		script_callback = 'hou.phm().length(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	length_template.setConditional(
		hou.parmCondType.HideWhen,
		'{ type_' + vis_id + ' != marker }')

	sep2_template = hou.SeparatorParmTemplate(
		name = 'sep2_' + vis_id)

	delvis_template = hou.ButtonParmTemplate(
		name = 'delvis_' + vis_id,
		label = "Delete Visualizer",
		script_callback = 'hou.phm().delvis(kwargs)',
		script_callback_language = hou.scriptLanguage.Python,
		join_with_next = True)

	foldername_template = hou.ButtonParmTemplate(
		name = 'foldername_' + vis_id,
		label = "Update Folder Name",
		script_callback = 'hou.phm().foldername(kwargs)',
		script_callback_language = hou.scriptLanguage.Python)

	folder_template = hou.FolderParmTemplate(
		name = 'folder_' + vis_id,
		label = "Vis " + vis_id,
		parm_templates = ([
			enable_template,
			attr_template,
			type_template,
			coloring_template,
			otherattr_template,
			sep1_template,
			preset_template,
			delpreset_template,
			interpol_template,
			ramp_template,
			color_template,
			length_template,
			sep2_template,
			delvis_template,
			foldername_template]),
		folder_type = hou.folderType.Tabs)

	group.appendToFolder(top_folder, folder_template)
	node.setParmTemplateGroup(group)

	##

	vis = hou.viewportVisualizers.createVisualizer(
		hou.viewportVisualizers.type('vis_color'),
		hou.viewportVisualizerCategory.Node,
		hou.node('./vis'))

	update(kwargs)

def enable(kwargs):
	parm = kwargs['parm']
	vis_id = parm.containingFolderIndices()[1]
	vis = getvis(vis_id)
	val = parm.evalAsInt()
	if val == 1:
		vis.setIsActive(True)
	if val == 0:
		vis.setIsActive(False)

def attr(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']
	vis_id = parm.containingFolderIndices()[1]
	val = parm.evalAsString()
	vis = getvis(vis_id)
	vis.setParm('attrib', val)

def type(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']
	val = parm.evalAsInt()
	vis_id = parm.containingFolderIndices()[1]

	vistypes = hou.viewportVisualizers.types()
	vis = getvis(vis_id)
	if val == 0:
		vis.setType(vistypes[1])
		vis.setParm('colortype', 1)
		vis.setParm('rangespec', 1)
		vis.setParm('clamptype', 1)
	if val == 1:
		vis.setType(vistypes[0])
		vis.setParm('style', 4)
		node.parm('coloring_' + str(vis_id)).pressButton()

def coloring(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	if parm.isHidden() == False:
		vis_id = parm.containingFolderIndices()[1]
		val = parm.evalAsInt()
		vis = getvis(vis_id)
		vis.setParm('vectorcoloring', val)
		if val == 0:
			node.parm('color_' + str(vis_id) + 'r').pressButton()
		if val != 0:
			vis.setParm('ramptype', 6)
			vis.setParm('rangespec', 0)
		if val == 3:
			node.parm('otherattr_' + str(vis_id)).pressButton()

def preset(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	if parm.isHidden() == False:
		val = parm.evalAsString()
		vis_id = parm.containingFolderIndices()[1]
		ramp_parm = node.parm('ramp_' + str(vis_id))
		
		if val == 'New...':
			newpreset(parm, ramp_parm)
			parm.set(0)
		if val == '_separator_':
			return
		if val != 'New...' and val != '_separator_':
			vis = getvis(vis_id)
			ramp_val = getattr(stain_schemes, val)
			ramp_parm.set(ramp_val)
			vis.setParm('colorramp', ramp_val)

def delpreset(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	vis_id = parm.containingFolderIndices()[1]
	preset_parm = node.parm('preset_' + str(vis_id))
	preset_val = preset_parm.evalAsString()

	menu = stain_menu.menu
	menu.remove(preset_val)
	menu.remove(preset_val)

	file = open('C:/Users/lucas/OneDrive/Git/morphogen/scripts/stain_menu.py', 'w')
	file.write('menu=' + str(menu))
	file.close()
	preset_parm.set(0)

	current_scheme = getattr(stain_schemes, preset_val)
	current_scheme = create_scheme(preset_val, current_scheme)

	path = 'C:/Users/lucas/OneDrive/Git/morphogen/scripts/stain_schemes.py'

	file = open(path, 'r').read()
	stain_schemes = file.replace(current_scheme, '')
	file.close()

	file = open(path, 'w')
	file.write(stain_schemes)
	write.close()

	importlib.reload(stain_menu)
	importlib.reload(stain_schemes)

def interpol(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	if parm.isHidden() == False:
		vis_id = parm.containingFolderIndices()[1]
		val = parm.evalAsString()

		ramp_parm = node.parm('ramp_' + str(vis_id))
		ramp_val = ramp_parm.evalAsRamp()
		
		basis = ramp_val.basis()
		keys = ramp_val.keys()
		values = ramp_val.values()
		
		new_basis = []
		for x in basis:
				new_basis.append(eval('hou.rampBasis.' + val))

		new_ramp = hou.Ramp(new_basis, keys, values)
		ramp_parm.set(new_ramp)
		
		vis = getvis(vis_id)
		vis.setParm('colorramp', new_ramp)

def ramp(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	if parm.isHidden() == False:
		val = parm.evalAsRamp()
		vis_id = parm.containingFolderIndices()[1]

		vis = getvis(vis_id)
		vis.setParm('colorramp', val)

def color(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	if parm.isHidden() == False:
		vis_id = parm.containingFolderIndices()[1]
		vis = getvis(vis_id)
		vis_id = str(vis_id)
		
		colorr = node.parm('color_' + vis_id + 'r').eval()
		colorg = node.parm('color_' + vis_id + 'g').eval()
		colorb = node.parm('color_' + vis_id + 'b').eval()

		vis.setParm('markercolorr', colorr)
		vis.setParm('markercolorg', colorg)
		vis.setParm('markercolorb', colorb)

def otherattr(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	if parm.isHidden() == False:
		vis_id = parm.containingFolderIndices()[1]
		vis = getvis(vis_id)
		val = node.parm('otherattr_' + str(vis_id)).evalAsString()
		vis.setParm('colorattrib', val)

def length(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	if parm.isHidden() == False:
		vis_id = parm.containingFolderIndices()[1]
		val = parm.evalAsFloat()
		vis = getvis(vis_id)
		vis.setParm('lengthscale', val)

def delvis(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']
	vis_id = parm.containingFolderIndices()[1]
	vis = getvis(vis_id)
	vis.destroy()

	group = node.parmTemplateGroup()
	top_folder = group.findFolder("Visualizers")
	bottom_folders = list(top_folder.parmTemplates())
	bottom_folders.pop(vis_id)
	top_folder.setParmTemplates(bottom_folders)
	group.replace((4,), top_folder)
	node.setParmTemplateGroup(group)

	vis_id = 0
	for bottom_folder in bottom_folders:
		rename(kwargs, vis_id, 'enable')
		rename(kwargs, vis_id, 'attr')
		rename(kwargs, vis_id, 'type')
		rename(kwargs, vis_id, 'coloring')
		rename(kwargs, vis_id, 'otherattr')
		rename(kwargs, vis_id, 'sep1')
		rename(kwargs, vis_id, 'preset')
		rename(kwargs, vis_id, 'delpreset')
		rename(kwargs, vis_id, 'interpol')
		rename(kwargs, vis_id, 'ramp')
		rename(kwargs, vis_id, 'color')
		rename(kwargs, vis_id, 'length')
		rename(kwargs, vis_id, 'sep2')
		rename(kwargs, vis_id, 'delvis')
		rename(kwargs, vis_id, 'foldername')
		vis_id += 1

	update(kwargs)

def rename(kwargs, vis_id, parmname):
	node = kwargs['node']
	vis_id = int(vis_id)

	group = node.parmTemplateGroup()
	top_folder = group.findFolder("Visualizers")
	bottom_folders = top_folder.parmTemplates()
	bottom_folder = bottom_folders[vis_id] 
	bottom_contents = bottom_folder.parmTemplates()

	for template in bottom_contents:
		split = template.name().split('_')[0]
		vis_id = str(vis_id)

		if split == parmname:
			template.setName(parmname + '_' + vis_id)

			if parmname == 'coloring':
				template.setConditional(
				hou.parmCondType.HideWhen,
				'{ type_' + vis_id + ' != marker }')

			if parmname == 'otherattr':
				template.setConditional(
				hou.parmCondType.HideWhen,
				'{ type_' + vis_id + ' != marker } { coloring_' + vis_id + ' != other }')

			if parmname == 'preset':
				template.setConditional(
				hou.parmCondType.HideWhen,
				'{ type_' + vis_id + ' == marker coloring_' + vis_id + ' == fixed }')

			if parmname == 'delpreset':
				template.setConditional(
				hou.parmCondType.HideWhen,
				'{ type_' + vis_id + ' == marker coloring_' + vis_id + ' == fixed }')

			if parmname == 'interpol':
				template.setConditional(
				hou.parmCondType.HideWhen,
				'{ type_' + vis_id + ' == marker coloring_' + vis_id + ' == fixed }')

			if parmname == 'ramp':
				template.setConditional(
				hou.parmCondType.HideWhen,
				'{ type_' + vis_id + ' == marker coloring_' + vis_id + ' == fixed }')

			if parmname == 'color':
				template.setConditional(
				hou.parmCondType.HideWhen,
				'{ type_' + vis_id + ' != marker } { coloring_' + vis_id + ' != fixed }')

			if parmname == 'length':
				template.setConditional(
				hou.parmCondType.HideWhen,
				'{ type_' + vis_id + ' != marker }')

	bottom_folder.setParmTemplates(bottom_contents)
	bottom_folders = list(bottom_folders)
	bottom_folders[int(vis_id)] = bottom_folder
	top_folder.setParmTemplates(bottom_folders)
	group.replace((4,), top_folder)
	node.setParmTemplateGroup(group)

def update(kwargs):
	node = kwargs['node']
	group = node.parmTemplateGroup()
	top_folder = group.findFolder("Visualizers")
	bottom_folders = list(top_folder.parmTemplates())
	
	vis_id = 0
	for bottom_folder in bottom_folders:
		vis_id = str(vis_id)
		node.parm('enable_' + vis_id).pressButton()
		node.parm('type_' + vis_id).pressButton()
		node.parm('attr_' + vis_id).pressButton()
		node.parm('preset_' + vis_id).pressButton()
		node.parm('coloring_' + vis_id).pressButton()
		node.parm('otherattr_' + vis_id).pressButton()
		node.parm('ramp_' + vis_id).pressButton()
		node.parm('color_' + vis_id + 'r').pressButton()
		node.parm('length_' + vis_id).pressButton()
		vis_id = int(vis_id)
		vis_id += 1

def foldername(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']
	vis_id = parm.containingFolderIndices()[1]

	attr_parm = node.parm('attr_' + str(vis_id))
	attr_val = attr_parm.evalAsString()
	group = node.parmTemplateGroup()
	top_folder = group.findFolder("Visualizers")
	bottom_folders = top_folder.parmTemplates()
	bottom_folders = list(bottom_folders)
	bottom_folder = bottom_folders[vis_id]
	if attr_val == '':
		bottom_folder.setLabel('vis' + str(vis_id))
	if attr_val != '':
		bottom_folder.setLabel(attr_val)
	bottom_folders[vis_id] = bottom_folder
	top_folder.setParmTemplates(bottom_folders)
	group.replace((4,), top_folder)
	node.setParmTemplateGroup(group)

def getvis(vis_id):
	vistup = hou.viewportVisualizers.visualizers(
		hou.viewportVisualizerCategory.Node,
		hou.node('./vis'))
	vis = vistup[int(vis_id)]
	return(vis)

def presetmenu():
	importlib.reload(stain_menu)
	menu = stain_menu.menu
	return(menu)

def newpreset(preset_parm, ramp_parm):
	new_name = hou.ui.readInput("New Preset", buttons = ("Add", "Cancel"))

	if new_name[0] == 0:
		menu = stain_menu.menu
		menu.insert(0, new_name[1])
		menu.insert(0, new_name[1])

		ramp_val = ramp_parm.evalAsRamp()
		new_scheme = create_scheme(new_name[1], ramp_val)
		
		menu_file = open('C:/Users/lucas/OneDrive/Git/morphogen/scripts/stain_menu.py', 'w')
		menu_file.write('menu=' + str(menu))
		menu_file.close()

		scheme_file = open('C:/Users/lucas/OneDrive/Git/morphogen/scripts/stain_schemes.py', 'a')
		scheme_file.write(new_scheme)
		scheme_file.close()

		importlib.reload(stain_menu)
		importlib.reload(stain_schemes)
		preset_parm.set(0)

def newscheme(preset_val, ramp_val):
	basis = ramp_val.basis()
	basis = tuple('hou.' + str(x) for x in basis)
	basis = str(basis).replace("'", "")

	keys = ramp_val.keys()
	keys = tuple(round(x, 4) for x in keys)

	values = ramp_val.values()
	values = tuple(tuple(round(x2, 4) for x2 in x) for x in values)

	scheme = '\n' + preset_val + '=' + 'hou.Ramp(' + str(basis) + ',' + str(keys) + ',' + str(values) + ')\n'

	return(scheme)