import hou
import importlib
import ramp_float_presets
import ramp_color_presets
import ramp_float_schemes
import ramp_color_schemes

def preset_float_callback(kwargs):
	importlib.reload(ramp_float_schemes)
	node = kwargs['node']
	preset_parm = kwargs['parm']
	preset_val = preset_parm.evalAsString()
	ramp_parm = node.parm('ramp_float')

	importlib.reload(ramp_float_presets)
	if preset_val == 'new':
		new_name = hou.ui.readInput("New Preset", buttons=("Add", "Cancel"))

		if new_name[0] == 0:
			presets = ramp_float_presets.presets
			presets.insert(0, new_name[1])
			presets.insert(0, new_name[1])
			presets_file = open('C:/Users/lucas/OneDrive/Git/morphogen/scripts/ramp_float_presets.py', 'w')
			presets_file.write('presets=' + str(presets))
			presets_file.close()

			ramp_basis = ramp_parm.eval().basis()
			ramp_keys = ramp_parm.eval().keys()
			ramp_values = ramp_parm.eval().values()
			new_scheme = (ramp_basis, ramp_keys, ramp_values)
			schemes_file = open('C:/Users/lucas/OneDrive/Git/morphogen/scripts/ramp_float_schemes.py', 'a')
			schemes_file.write('\n' + new_name[1] + '=Ramp' + str(new_scheme))
			schemes_file.close()

			importlib.reload(ramp_float_presets)
			importlib.reload(ramp_float_schemes)
			preset_parm.set(0)

	else:
		new_ramp_val = getattr(ramp_float_schemes, preset_val)
		ramp_parm.set(new_ramp_val)

def del_preset_float_callback(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']

	preset_parm = node.parm('preset_float')
	preset_val = preset_parm.evalAsString()
	presets = ramp_float_presets.presets
	presets.remove(preset_val)
	presets.remove(preset_val)
	presets_file = open('C:/Users/lucas/OneDrive/Git/morphogen/scripts/ramp_float_presets.py', 'w')
	presets_file.write('presets=' + str(presets))
	presets_file.close()
	preset_parm.set(0)

	scheme = getattr(ramp_float_schemes, preset_val)
	basis = scheme.basis()
	keys = scheme.keys()
	values = scheme.values()
	scheme = preset_val + '=Ramp' + str((basis, keys, values))
	# print(scheme)

	schemes_file_path = 'C:/Users/lucas/OneDrive/Git/morphogen/scripts/ramp_float_schemes.py'

	schemes_file = open(schemes_file_path, 'r')
	schemes_str = schemes_file.read()
	schemes_file.close()
	schemes = schemes_str.replace(scheme, '')

	schemes_file = open(schemes_file_path, 'w')
	schemes_file.write(schemes)
	schemes_file.close()

	importlib.reload(ramp_float_presets)
	importlib.reload(ramp_float_schemes)

def interpolation_float_callback(kwargs):
	node = kwargs['node']
	interpolation_parm = kwargs['parm']
	interpolation_val = interpolation_parm.evalAsString()
	ramp_parm = node.parm('ramp_float')
	ramp_basis = ramp_parm.eval().basis()
	new_basis = []
	for basis in ramp_basis:
		new_basis.append(eval('hou.rampBasis.' + interpolation_val))
	ramp_keys = ramp_parm.eval().keys()
	ramp_values = ramp_parm.eval().values()
	new_ramp_val = hou.Ramp(new_basis, ramp_keys, ramp_values)
	ramp_parm.set(hou.Ramp(new_basis, ramp_keys, ramp_values))

def attr_menu_callback(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']
	val_str = parm.evalAsString()
	val_int = parm.evalAsInt()
	attr_parm = node.parm('attr')
	attr_parm.set(val_str)

	index = node.parm('index').evalAsInt()
	data_parm = node.parm('data')
	if val_int < index:
		data_parm.set(0)
	else:
		data_parm.set(1)

def attr_callback(kwargs):
	node = kwargs['node']
	parm = kwargs['parm']
	
	parm_int = parm.evalAsInt()
	print(parm_int)
	index = node.parm('index').evalAsInt()