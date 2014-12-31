# Prip
# Main Program

import sys
import os
from PyQt4 import QtCore, QtGui, uic
from functools import partial

from PripGraphicsScene import PripGraphicsScene


# Load the UI
path = ""
form_class = uic.loadUiType(path + "PRip.ui")[0]

class Main_Window(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self._graphicsScene = PripGraphicsScene(self)
        self.graphicsView.setScene(self._graphicsScene)
        #self.graphicsView.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

        # Line edit events
        for lineEdit in [self.lineEditX0, self.lineEditX1,
                         self.lineEditY0, self.lineEditY1]:
            # Add validators
            lineEdit.setValidator(QtGui.QDoubleValidator(-1e10, 1e10,
                                                         10, lineEdit));
            # Connect events
            self.connect(lineEdit,
                         QtCore.SIGNAL("textEdited(QString)"),
                         self.read_axis_references)

        # Button events
        self.connect(self.pushButtonPlaceX0,
                     QtCore.SIGNAL("clicked()"),
                     partial(self._graphicsScene.set_insert_mode,
                             PripGraphicsScene.InsertMode.X0))
        self.connect(self.pushButtonPlaceX1,
                     QtCore.SIGNAL("clicked()"),
                     partial(self._graphicsScene.set_insert_mode,
                             PripGraphicsScene.InsertMode.X1))
        self.connect(self.pushButtonPlaceY0,
                     QtCore.SIGNAL("clicked()"),
                     partial(self._graphicsScene.set_insert_mode,
                             PripGraphicsScene.InsertMode.Y0))
        self.connect(self.pushButtonPlaceY1,
                     QtCore.SIGNAL("clicked()"),
                     partial(self._graphicsScene.set_insert_mode,
                             PripGraphicsScene.InsertMode.Y1))

        # Actions
        self.connect(self.actionNew,
                        QtCore.SIGNAL("triggered()"),
                        self.new_project)
        self.connect(self.actionOpen_Project,
                        QtCore.SIGNAL("triggered()"),
                        self.open_project)
        self.connect(self.actionSave_Project,
                        QtCore.SIGNAL("triggered()"),
                        self.save_project)
        self.connect(self.actionSave_Project_As,
                        QtCore.SIGNAL("triggered()"),
                        self.save_project_as)
        self.connect(self.actionExit,
                        QtCore.SIGNAL("triggered()"),
                        self.exit)

        # Mouse move
        self._graphicsScene.mouse_moved.connect(self.update_mouse_pos_status_bar)

    @QtCore.pyqtSlot(float, float)
    def update_mouse_pos_status_bar(self, x, y):
        self.statusBar().showMessage("x=%f, y=%f" % (x,y))

    def new_project(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,
            'Select plot image to rip', path,
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tif)")
        if filename is not None and not str(filename) == "":
            # Clean previous state
            self._graphicsScene.new_project(filename)
            self.file_name = None
            self.update_interface()

    def open_project(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,
            'Select PRip project', path,
            "PRip project (*.prip)")
        if filename is not None and not str(filename) == "":
            # Try to load project
            if self._graphicsScene.load_project(filename):
                self.file_name = filename
                self.update_interface()

    def save_project(self):
        if self.file_name is None:
            self.save_project_as()
        else:
            self._graphicsScene.save_project(self.file_name)

    def save_project_as(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,
            'Select PRip project', path,
            "PRip project (*.prip)")
        if filename is not None and not str(filename) == "":
            self.file_name = filename
            self.save_project()

    def exit(self):
        self.close()

    def read_axis_references(self):
        try:
            self._graphicsScene.x0 = float(self.lineEditX0.text())
        except: pass
        try:
            self._graphicsScene.x1 = float(self.lineEditX1.text())
        except: pass
        try:
            self._graphicsScene.y0 = float(self.lineEditY0.text())
        except: pass
        try:
            self._graphicsScene.y1 = float(self.lineEditY1.text())
        except: pass

    def update_interface(self):
        self.graphicsView.setEnabled(True)
        self.update_axis_references()

    def update_axis_references(self):
        self.lineEditX0.setText(str(self._graphicsScene.x0))
        self.lineEditX1.setText(str(self._graphicsScene.x1))
        self.lineEditY0.setText(str(self._graphicsScene.y0))
        self.lineEditY1.setText(str(self._graphicsScene.y1))


if __name__ == '__main__':
    # Entry point
    aplication = QtGui.QApplication(sys.argv)
    main_window = Main_Window(None)
    main_window.show()

    sys.exit(aplication.exec_())
