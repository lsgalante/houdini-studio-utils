import hou

class DefaultCam:
    def __init__(self, hou_defaultcam):
        self.hou_defaultcam = hou_defaultcam

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
