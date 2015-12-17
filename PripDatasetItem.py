# Prip
# class PripDatasetItem

from PyQt4 import QtCore, QtGui, uic
import pickle

class PripDatasetItem(QtGui.QListWidgetItem):

    def __init__(self, key, name):
        QtGui.QListWidgetItem.__init__(self, None)

        self._key = key
        self._name = name
        self.setText(name)
