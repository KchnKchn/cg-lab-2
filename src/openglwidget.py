from PyQt5 import QtCore, QtOpenGL

class glWidget(QtOpenGL.QGLWidget):

    initialize = QtCore.pyqtSignal()
    resize = QtCore.pyqtSignal(int, int)
    render = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

    def initializeGL(self):
        self.initialize.emit()

    def paintGL(self):
        self.render.emit()
    
    def resizeGL(self, width: int, height: int):
        self.resize.emit(width, height)
