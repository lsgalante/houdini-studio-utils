import hou

class HCDefaultCam:
    def __init__(self, default_cam):
        self.default_cam = default_cam

    def frame(self):
        for viewport in self.viewports():
            hou_defaultcam = viewport.camera()
            # Is cam default or node.
            if not hou_defaultcam:
                viewport.frameAll()

    def nextView(self):
        return

    def rotate(self, key):
        return

    def translate(self, key):
        return

    def zoom(self):
        return
