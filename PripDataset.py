# Prip
# class PripDataset

from PyQt4 import QtCore, QtGui, uic
import PripGraphicsView
from vector import *
import pickle

class PripDataset(QtGui.QListWidgetItem):
    # Signal emitted when the mouse is moved
    # mouse_moved = QtCore.pyqtSignal(float, float)

    def __init__(self, name = "New Dataset"):
        QtGui.QListWidgetItem.__init__(self, None)

        self._name = name
        self.setText(self._name)
