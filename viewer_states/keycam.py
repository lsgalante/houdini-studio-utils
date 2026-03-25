import hou
from hc import Cam, Geo, Guides, SceneViewer


def createViewerStateTemplate():
    template = hou.ViewerStateTemplate(
        type_name='keycam', label='keycam',
        category=hou.objNodeTypeCategory(),
        contexts=[hou.sopNodeTypeCategory()]
    )

    template.bindFactory(State)
    template.bindIcon('DESKTOP_application_sierra')

    # Parameters

    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='layout', label='Layout',
        default_value='single',
        menu_items=[
            ('doubleside',        'DoubleSide'),
            ('doublestack',       'DoubleStack'),
            ('quad',              'Quad'),
            ('quadbottomsplit',   'QuadBottomSplit'),
            ('quadleftsplit',     'QuadLeftSplit'),
            ('single',            'Single'),
            ('triplebottomsplit', 'TripleBottomSplit'),
            ('tripleleftsplit',   'TripleLeftSplit')
        ]
    )

    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='viewport', label='Viewport',
        default_value='center',
        menu_items=[('center', 'Center')]
    )

    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='view', label='View',
        default_value='persp',
        menu_items=[
            ('persp',  'Perspective'),
            ('top',    'Top'),
            ('front',  'Front'),
            ('right',  'Right'),
            ('uv',     'UV'),
            ('bottom', 'Bottom'),
            ('back',   'Back'),
            ('left',   'Left')
        ]
    )

    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='camera', label='Camera',
        default_value='keycam',
        menu_items=[
            ('keycam',  'Keycam'),
            ('default', 'Default'),
            ('other',   'Other')
        ],
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='target', label='Target',
        default_value='cam',
        menu_items=[
            ('cam',   'Camera'),
            ('pivot', 'Pivot')
        ],
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Separator,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='t', label='Translation',
        num_components=3,
        toolbox=False
    )

    # template.bindParameter(
    #     hou.parmTemplateType.Float,
    #     name='r', label='Rotation',
    #     num_components=3,
    #     toolbox=False
    # )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='p', label='Pivot',
        num_components=3,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='zoom', label='Zoom',
        num_components=1,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='ow', label='Ortho Width',
        num_components=1,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Separator,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='delta_t', label='Delta T',
        default_value=1.0,
        min_limit=0, max_limit=10.0
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='delta_r', label='Delta R',
        default_value=15.0,
        min_limit=-180.0, max_limit=180.0
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='delta_zoom', label='Delta Zoom',
        default_value=1.0,
        min_limit=0, max_limit=10.0
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='delta_ow', label='Delta OW',
        default_value=1.0,
        min_limit=0, max_limit=10.0
    )


    """ Context Menu """

    menu = hou.ViewerStateMenu('keycam_menu', 'Keycam Menu')
    menu.addActionItem('frame', 'Frame')
    menu.addActionItem('reset', 'Reset')

    setViewMenu = hou.ViewerStateMenu('set_view_menu', 'Set View')
    setViewMenu.addActionItem('top',    'Top')
    setViewMenu.addActionItem('bottom', 'Bottom')
    setViewMenu.addActionItem('front',  'Front')
    setViewMenu.addActionItem('back',   'Back')
    setViewMenu.addActionItem('left',   'Left')
    # setViewMenu.addActionItem('right', 'Right')
    menu.addMenu(setViewMenu)

    guideMenu = hou.ViewerStateMenu('guide_menu', 'Guides')
    guideMenu.addToggleItem('bbox',       'Bbox',        0)
    guideMenu.addToggleItem('cam_axis',   'Camera Axis', 0)
    guideMenu.addToggleItem('pivot_axis', 'Pivot Axis',  0)
    guideMenu.addToggleItem('perim',      'Perimeter',   0)
    guideMenu.addToggleItem('pivot_2d',   '2D Pivot',    0)
    guideMenu.addToggleItem('pivot_3d',   '3D Pivot',    0)
    guideMenu.addToggleItem('ray',        'Ray',         0)
    menu.addMenu(guideMenu)

    menu.addSeparator()
    template.bindMenu(menu)

    # Ok
    return template


class State(object):
    def __init__(self, state_name, scene_viewer):
        self.options = {
            'center_on_geo': 1,
            'lock_cam':      1,
            'reset':         0
        }

        """ Check for cam node """
        if not hou.node('/obj/keycam'):
            cam_node = hou.node('/obj').createNode('cam')
            cam_node.setName('keycam')
            cam_node.parm('xOrd').set(0)
        self.cam_node = hou.node('/obj/keycam')

        self.hou_scene_viewer = scene_viewer
        self.scene_viewer = None
        self.state_name = state_name
        self.cam = None
        # self.default_cam = DefaultCam(self, hou_default_cam)
        self.kwargs = None
        self.guides = None
        self.hud = None

    def onDraw(self, kwargs):
        self.guides.draw(kwargs)

    def onExit(self, kwargs):
        for viewport in self.scene_viewer.allViewports():
            viewport.lockCameraToView(False)

    def onGenerate(self, kwargs):
        self.kwargs = kwargs
        self.scene_viewer = SceneViewer(self.hou_scene_viewer)
        self.cam = Cam(self.cam_node, self.hou_scene_viewer)
        self.guides = Guides(self)
        """ Prevent exiting state when current node changes """
        self.kwargs['state_flags']['exit_on_node_select'] = False
        self.guides.update()
        self.hud = Hud(self)
        self.hud.update()

    def onKeyEvent(self, kwargs):
        self.cam.fitAspectRatio()

        key_map = {
            'o':       self.cam.toggleProjection,
            'h':       self.cam.rotateLeft,
            'j':       self.cam.rotateDown,
            'k':       self.cam.rotateUp,
            'l':       self.cam.rotateRight,
            # 'v':       self.scene_viewer.nextView,
            'Shift+h': self.cam.translateLeft,
            'Shift+j': self.cam.translateDown,
            'Shift+k': self.cam.translateUp,
            'Shift+l': self.cam.translateRight,
            # 'Ctrl+l':  self.scene_viewer.nextLayout,
            'f':       self.cam.frame
            # 'c':       self.cam.center
        }

        key_map_persp = {
            '-':       lambda: self.cam.zoom('out'),
            '=':       lambda: self.cam.zoom('in'),
            'Shift+-': lambda: self.cam.zoomOrtho('out'),
            'Shift+=': lambda: self.cam.zoomOrtho('in')
        }

        key_map_ortho = {
            '-':       lambda: self.cam.zoomOrtho('out'),
            '=':       lambda: self.cam.zoomOrtho('in'),
            'Shift+-': lambda: self.cam.zoom('out'),
            'Shift+=': lambda: self.cam.zoom('in')
        }

        if self.cam.projection == 'perspective':
            key_map.update(key_map_persp)
        else:
            key_map.update(key_map_ortho)

        key = kwargs['ui_event'].device().keyString()

        if key in key_map:
            key_map[key]()
            print(self.cam.p)
            print(self.cam.t)
            print(self.cam.r)
            self.guides.update()
            return True
        else:
            return False

    def onMenuAction(self, kwargs):
        menu_item = kwargs['menu_item']
        guides = self.guides

        action_map = {
            'frame': self.cam.frame,
            'reset': self.cam.reset
        }

        if menu_item in action_map:
            return action_map[menu_item]()
        else:
            self.guides.states[menu_item] = kwargs[menu_item]
            return

    def onMenuPreOpen(self, kwargs):
        menu_id = kwargs['menu']
        item_states = kwargs['menu_item_states']

        """ Set the checkbox states when opening guide menu """
        if menu_id == 'guide_menu':
            item_states['cam_axis']['value']   = self.guides.cam_axis.visible()
            item_states['pivot_axis']['value'] = self.guides.pivot_axis.visible()
            item_states['bbox']['value']       = self.guides.bbox.visible()
            item_states['perim']['value']      = self.guides.perim.visible()
            item_states['pivot_2d']['value']   = self.guides.pivot_2d.visible()
            item_states['pivot_3d']['value']   = self.guides.pivot_3d.visible()
            item_states['ray']['value']        = self.guides.ray.visible()

    def onParmChangeEvent(self, kwargs):
        parm_map = {
            't':          (self.cam, 't'),
            'p':          (self.cam, 'p'),
            'r':          (self.cam, 'r'),
            'ow':         (self.cam, 'ow'),
            'zoom':       (self.cam, 'zoom'),
            'target':     (self.cam, 'target'),
            'delta_r':    (self.cam, 'delta_r'),
            'delta_t':    (self.cam, 'delta_t'),
            'delta_zoom': (self.cam, 'delta_zoom'),
            # 'delta_ow':   (self.cam, 'delta_ow'),
            # 'layout':     (self.cam, 'layout'),
            'viewport':   (self.cam, 'viewport'),
            # 'view':       (self.cam, 'view'),
            # 'camera':     (self.cam, 'camera'),
        }

        obj = parm_map[kwargs['parm_name']][0]
        attr = parm_map[kwargs['parm_name']][1]
        setattr(obj, attr, kwargs['parm_value'])
        # self.guides.update


class Hud:
    def __init__(self, state):
        self.state            = state
        self.hou_scene_viewer = state.hou_scene_viewer
        self.scene_viewer     = state.scene_viewer
        self.template         = {
            'title': 'Keycam',
            'rows': [
                {
                    'id':    'layout',
                    'type':  'plain',
                    'label': 'Layout',
                    'value': 'Single',
                    'key':   'Ctrl + L'
                },
                {
                    'id':    'layout_g',
                    'type':  'choicegraph',
                    'count': 8
                },
                {
                    'id':    'viewport',
                    'type':  'plain',
                    'label': 'Viewport',
                    'value': '0',
                    'key':   'Ctrl + V'
                },
                {
                    'id':    'viewport_g',
                    'type':  'choicegraph',
                    'count': 4
                },
                {
                    'id':    'view',
                    'type':  'plain',
                    'label': 'View',
                    'value': 'Perspective',
                    'key':   'V'
                },
                {
                    'id':    'view_g',
                    'type':  'choicegraph',
                    'count': 8
                },
                {
                    'id':    'target',
                    'type':  'plain',
                    'label': 'Target',
                    'value': 'Camera',
                    'key':   'T'
                },
                {
                    'id':    'target_g',
                    'type':  'choicegraph',
                    'count': 2
                },
                {
                    'id':    'vis',
                    'type':  'plain',
                    'label': 'Vis'
                },
                {
                    'id':    'focus',
                    'type':  'plain',
                    'label': 'Focus',
                    'value': 0
                },
                {
                    'id':    'focus_g',
                    'type':  'choicegraph',
                    'count': 10
                }
            ]
        }

    def update(self):
        layout_map = {
            'geometryViewportLayout.DoubleSide':        2,
            'geometryViewportLayout.DoubleStack':       2,
            'geometryViewportLayout.Quad':              4,
            'geometryViewportLayout.QuadBottomSplit':   4,
            'geometryViewportLayout.QuadLeftSplit':     4,
            'geometryViewportLayout.TripleBottomSplit': 3,
            'geometryViewportLayout.TripleLeftSplit':   3,
            'geometryViewportLayout.Single':            1,
        }
        layout = self.scene_viewer.layout()
        n_viewports = layout_map[str(layout)]
        self.template['rows'][3]['count'] = n_viewports

        # Updates
        self.hou_scene_viewer.hudInfo(template=self.template)
        updates = {
            'layout':   str(self.scene_viewer.layout())[23:],
            'layout_g': self.scene_viewer.layouts().index(self.scene_viewer.layout()),
        }
        self.hou_scene_viewer.hudInfo(hud_values=updates)
