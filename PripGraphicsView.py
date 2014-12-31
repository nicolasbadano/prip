# Prip
# class PripGraphicsView

from PyQt4 import QtCore, QtGui, uic

class PripGraphicsView(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)

        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, evt):
        # Update scale
        if evt.delta() > 0:
            self.scale(1.1, 1.1)
        else:
            self.scale(1.0/1.1, 1.0/1.1)

