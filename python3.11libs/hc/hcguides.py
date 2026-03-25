import hou

class HCGuides:
    def __init__(self, state):
        self.state = state
        self.cam_node = state.cam_node
        self.cam = state.cam
        self.scene_viewer = hou_scene_viewer
        self.hc_scene_viewer = hc_state.scene_viewer

        self.options = {
            'axis_size': 1,
            'tie_axis_to_radius': 0
        }

        self.states = {
            'cam_axis': 0,
            'pivot_axis': 1,
            'bbox': 0,
            'perim': 0,
            'pivot_2d': 0,
            'pivot_3d': 0,
            'ray': 0
        }

        self.cam_axis = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='cam_axis'
        )

        self.pivot_axis = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='pivot_axis',
            params={
                'color1': hou.Vector4((1, 1, 1, 0.5))
            }
        )

        self.bbox = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='bbox',
            params={
                'color1': hou.Vector4((1, 1, 1, 0.3)),
                'fade_factor': 0.0
            }
        )

        self.perim = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='perim'
        )

        self.pivot_2d = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='pivot_2d'
        )

        self.pivot_3d = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Face,
            name='pivot_3d',
            params={
                'color1': hou.Vector4(0.2, 0.8, 0.2, 0.6),
                'fade_factor': 0.2
            }
        )

        self.ray = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='ray',
            params={
                'color1': hou.Vector4((1, 0.8, 1, 0.5))
            }
        )

    def draw(self, kwargs):
        func_map = {
            'bbox':       self.bbox.draw,
            'cam_axis':   self.cam_axis.draw,
            'pivot_axis': self.pivot_axis.draw,
            'perim':      self.perim.draw,
            'pivot_2d':   self.pivot_2d.draw,
            'pivot_3d':   self.pivot_3d.draw,
            'ray':        self.ray.draw
        }
        for name, value in self.states.items():
            if value:
                func_map[name](kwargs['draw_handle'], {})

    def update(self):
        func_map = {
            'bbox':       self.makeBbox,
            'cam_axis':   self.makeCamAxis,
            'pivot_axis': self.makePivotAxis,
            'perim':      self.makePerim,
            'pivot_2d':   self.makePivot2d,
            'pivot_3d':   self.makePivot3d,
            'ray':        self.makeRay
        }
        for name, value in self.states.items():
            if value:
                func_map[name]()
        # self.cam_axis.show(self.states['cam_axis'])
        self.pivot_axis.show(self.states['pivot_axis'])
        self.bbox.show(self.states['bbox'])
        # self.cam.show(self.states['cam'])
        # self.perim.show(self.states['perim'])
        # self.pivot_2d.show(self.states['pivot_2d'])
        self.pivot_3d.show(self.states['pivot_3d'])
        # self.ray.show(self.states['ray'])


    """ Construction """

    def makeCamAxis(self):
        axes = (
            self.hc_cam.local_x,
            self.hc_cam.local_y,
            self.hc_cam.local_z
        )
        geo = hou.Geometry()
        for i in range(3):
            P0 = self.hc_cam.t + axes[i]
            P1 = self.hc_cam.t + axes[i] * -1
            pts = geo.createPoints((P0, P1))
            poly = geo.createPolygon(is_closed=False)
            poly.addVertex(pts[0])
            poly.addVertex(pts[1])
        self.cam_axis.setGeometry(geo)

    def makePivotAxis(self):
        axes = (
            self.cam.local_x,
            self.cam.local_y,
            self.cam.local_z
            # hou.Vector3(1, 0, 0),
            # hou.Vector3(0, 1, 0),
            # hou.Vector3(0, 0, 1)
        )
        colors = (
            [1.0, 0.7, 0.7],
            [0.7, 1.0, 0.7],
            [0.7, 0.7, 1.0]
        )
        geo = hou.Geometry()
        geo.addAttrib(hou.attribType.Point, 'Cd', (0.1, 0.1, 0.1))
        for i in range(3):
            P0 = self.hc_cam.p + axes[i]
            P1 = self.hc_cam.p + axes[i] * -1
            pts = geo.createPoints((P0, P1))
            pts[0].setAttribValue('Cd', colors[i])
            pts[1].setAttribValue('Cd', colors[i])
            poly = geo.createPolygon(is_closed=False)
            poly.addVertex(pts[0])
            poly.addVertex(pts[1])
        self.pivot_axis.setGeometry(geo)
        self.pivot_axis.setParams(
            {'fade_factor': 0.0}
        )

    def makeBbox(self):
        guide_geo = hou.Geometry()
        target_geo = self.hc_scene_viewer.geo()
        bbox = target_geo.bbox()
        box = hou.sopNodeTypeCategory().nodeVerb('box')
        box.setParms(
            {
                'size': bbox.sizevec(),
                't':    bbox.center()
            }
        )
        box.execute(guide_geo, [])
        self.bbox.setGeometry(guide_geo)

    def makePerim(self):
        guide_geo = hou.Geometry()
        circle = hou.sopNodeTypeCategory().nodeVerb('circle')
        circle.setParms(
            {
                'divs': 128,
                'type': 1,
                't':    self.hc_cam.p,
                'scale': self.hc_cam.p.distanceTo(self.cam.t),
                'orient': 2
            }
        )
        circle.execute(guide_geo, [])
        self.perim.setParams(
            {
                'color1': hou.Vector4(1.0, 1.0, 1.0, 0.25),
                'fade_factor': 1.0
            }
        )
        self.perim.setGeometry(guide_geo)

    def makePivot2d(self):
        guide_geo = hou.Geometry()
        circle = hou.sopNodeTypeCategory().nodeVerb('circle')
        circle.setParms(
            {
                'type': 1,
                'r':    self.cam.r,
                't':    self.cam.p,
                'scale': self.cam.ow * 0.0075
            }
        )
        circle.execute(guide_geo, [])
        self.pivot_2d.setParams(
            {
                'color1': hou.Vector4(0.0, 0.0, 1, 1),
                'fade_factor': 1.0
            }
        )
        self.pivot_2d.setGeometry(guide_geo)

    def makePivot3d(self):
        guide_geo = hou.Geometry()
        sphere = hou.sopNodeTypeCategory().nodeVerb('sphere')
        scale = self.cam.t.distanceTo(self.cam.p) * 0.01
        sphere.setParms(
            {
                'freq':  7,
                'scale': scale,
                'type':  1,
                't':     self.hc_cam.p
            }
        )
        sphere.execute(guide_geo, [])
        self.pivot_3d.setGeometry(guide_geo)

    def makeRay(self):
        guide_geo = hou.Geometry()
        guide_geo.addAttrib(hou.attribType.Point, 'Cd', (1, 0, 0))
        pts = guide_geo.createPoints((self.hc_cam.p, self.hc_cam.t))
        poly = guide_geo.createPolygon()
        poly.addVertex(pts[0])
        poly.addVertex(pts[1])
        self.ray.setGeometry(guide_geo)
