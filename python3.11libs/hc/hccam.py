import hou
from .hcgeo import HCGeo
from .hcsceneviewer import HCSceneViewer

"""
Accepts 1 camera node object and 1 scene viewer object as arguments.
"""

class HCCam:
    def __init__(self, node, scene_viewer):
        self.node = node
        self.scene_viewer = scene_viewer
        self.hc_scene_viewer = HCSceneViewer(scene_viewer)
        self.node = node
        self._t            = hou.Vector3(0, 0, 0)
        self._r            = hou.Vector3(0, 0, 0)
        self._p            = hou.Vector3(0, 0, 0)
        self._ow           = 10
        self._projection   = 'perspective'
        self._resx         = 1000
        self._resy         = 1000
        self._aspect_ratio = 1
        self.local_x       = hou.Vector3(1, 0, 0)
        self.local_y       = hou.Vector3(0, 1, 0)
        self.local_z       = hou.Vector3(0, 0, 1)
        self.global_x      = hou.Vector3(1, 0, 0)
        self.global_y      = hou.Vector3(0, 1, 0)
        self.global_z      = hou.Vector3(0, 0, 1)
        # self.zoom          = 10
        self.delta_t       = 1
        self.delta_r       = 15
        self.delta_zoom    = 1
        self.target        = None

        self.fitAspectRatio()
        self.lock()
        self.reset()

    """ Movement """

    def center(self):
        centroid = self.hc_scene_viewer.geo().centroid()
        self.t = hou.Vector3(centroid)
        self.p = hou.Vector3(centroid)

    def frame(self):
        centroid = self.geo().centroid()
        self.t = hou.Vector3(centroid)
        self.p = hou.Vector3(centroid)
        # self.ow = 10
        self.setZoom(10)

    def home(self):
        centroid = self.geo().centroid()
        self.t = centroid
        self.p = centroid
        # self.ow = 10
        # self.setZoom(6)

    # def movePivot(self):
        # If origin
        # if self.target == 0:
        #     self.t = [0, 0, self.zoom]
        #     self.r = [45, 45, 0]
        #     self.p = [0, 0, self.zoom * -1]
        #     self.ow = 10

    def rotateUp(self):
        delta = hou.Vector3(self.delta_r, 0, 0)
        self.r += delta
        m = hou.hmath.buildRotateAboutAxis(self.local_x, self.delta_r)
        self.t -= self.p
        self.t *= m
        self.t += self.p
        self.local_x *= m
        self.local_y *= m
        self.local_z *= m

    def rotateDown(self):
        delta = hou.Vector3(-self.delta_r, 0, 0)
        self.r += delta
        m = hou.hmath.buildRotateAboutAxis(self.local_x, -self.delta_r)
        self.t -= self.p
        self.t *= m
        self.t += self.p
        self.local_x *= m
        self.local_y *= m
        self.local_z *= m

    def rotateLeft(self):
        delta = hou.Vector3(0, -self.delta_r, 0)
        self.r += delta
        m = hou.hmath.buildRotateAboutAxis(self.global_y, -self.delta_r)
        self.t -= self.p
        self.t *= m
        self.t += self.p
        self.local_x *= m
        self.local_y *= m
        self.local_z *= m

    def rotateRight(self):
        delta = hou.Vector3(0, self.delta_r, 0)
        self.r += delta
        m = hou.hmath.buildRotateAboutAxis(self.global_y, self.delta_r)
        self.t -= self.p
        self.t *= m
        self.t += self.p
        self.local_x *= m
        self.local_y *= m
        self.local_z *= m

    def setZoom(self, amt):
        move = self.local_z * amt
        self.t += move

    def translateUp(self):
        move = self.local_y * self.delta_t
        self.t += move
        self.p += move

    def translateDown(self):
        move = self.local_y * self.delta_t * -1
        self.t += move
        self.p += move

    def translateLeft(self):
        move = self.local_x * self.delta_t * -1
        self.t += move
        self.p += move

    def translateRight(self):
        move = self.local_x * self.delta_t
        self.t += move
        self.p += move

    def zoom(self, dir):
        dir_map = {'out': 1, 'in': -1}
        move = self.local_z * self.delta_zoom * dir_map[dir]
        self.t += move

    def zoomOrtho(self, dir):
        dir_map = {'out': 1, 'in': -1}
        self.ow += self.delta_zoom * dir_map[dir]


    """ Props """

    @property
    def t(self):
        return self._t
    @t.setter
    def t(self, val):
        self._t = val
        self.node.parmTuple('t').set(val)

    @property
    def r(self):
        return self._r
    @r.setter
    def r(self, val):
        self._r = val
        self.node.parmTuple('r').set(val)

    @property
    def p(self):
        return self._p
    @p.setter
    def p(self, val):
        self._p = val

    @property
    def ow(self):
        return self._ow
    @ow.setter
    def ow(self, val):
        self._ow = val
        self.node.parm('orthowidth').set(val)

    @property
    def projection(self):
        return self._projection
    @projection.setter
    def projection(self, val):
        self._projection = val
        self.node.parm('projection').set(val)

    @property
    def resx(self):
        return self._resx
    @resx.setter
    def resx(self, val):
        self._resx = val
        self.node.parm('resx').set(val)

    @property
    def resy(self):
        return self._resy
    @resy.setter
    def resy(self, val):
        self._resy = val
        self.node.parm('resy').set(val)

    @property
    def aspect_ratio(self):
        return self._aspect_ratio
    @aspect_ratio.setter
    def aspect_ratio(self, val):
        self._aspect_ratio = val
        self.node.parm('aspect').set(val)

    """ Util """

    def fitAspectRatio(self):
        self.resx = 1000
        self.resy = 1000
        ratio = self.viewport().size()[2] / self.viewport().size()[3]
        self.aspect_ratio = ratio

    def geo(self):
        return self.hc_scene_viewer.geo()

    def lock(self):
        hc_viewport = self.hc_viewport()
        hc_viewport.setCamera(self.node)
        hc_viewport.lockCameraToView(1)

    def reset(self):
        self.t          = hou.Vector3(0, 0, 2)
        self.r          = hou.Vector3(0, 0, 0)
        self.p          = hou.Vector3(0, 0, 0)
        # self.zoom       = 10
        self.ow         = 10
        self.delta_t    = 1
        self.delta_r    = 15
        self.delta_zoom = 1
        self.local_x    = hou.Vector3(1, 0, 0)
        self.local_y    = hou.Vector3(0, 1, 0)
        self.local_z    = hou.Vector3(0, 0, 1)
        self.global_x   = hou.Vector3(1, 0, 0)
        self.global_y   = hou.Vector3(0, 1, 0)
        self.global_z   = hou.Vector3(0, 0, 1)

    def setView(self):
        view_map = {
            'top':    hou.Vector3(270, 0, 0),
            'bottom': hou.Vector3(90, 0, 0),
            'front':  hou.Vector3(0, 180, 0),
            'back':   hou.Vector3(0, 0, 0),
            'right':  hou.Vector3(0, 90, 0),
            'left':   hou.Vector3(0, 270, 0)
        }
        self.r = view_map[self.view]

    def toggleProjection(self):
        projection_map = {
            'perspective': 'ortho',
            'ortho':       'perspective'
        }
        self.projection = projection_map[self.projection]

    def unlock(self):
        self.viewport().lockCameraToView(0)

    def viewport(self):
        return self.hc_scene_viewer.allViewports()[3]

