#!/usr/bin/env python

# Prip
# Main Program

import sys
from PyQt4 import QtCore, QtGui, uic
from functools import partial

from PripModel import PripModel
from PripView import PripView
from PripGraphicsScene import PripGraphicsScene
from PripInsertMode import PripInsertMode
from PripGraphicsRectItem import PripGraphicsRectItem

# Load the UI
path = ""
form_class = uic.loadUiType(path + "PRip.ui")[0]

class Main_Window(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.file_name = None
        self.model = PripModel()

        self.model.model_changed.connect(self.update_interface)

        self._graphicsScene = PripGraphicsScene(self)
        self.graphicsView.setScene(self._graphicsScene)

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
                     partial(self.model.set_insert_mode,
                             PripInsertMode.X0))
        self.connect(self.pushButtonPlaceX1,
                     QtCore.SIGNAL("clicked()"),
                     partial(self.model.set_insert_mode,
                             PripInsertMode.X1))
        self.connect(self.pushButtonPlaceY0,
                     QtCore.SIGNAL("clicked()"),
                     partial(self.model.set_insert_mode,
                             PripInsertMode.Y0))
        self.connect(self.pushButtonPlaceY1,
                     QtCore.SIGNAL("clicked()"),
                     partial(self.model.set_insert_mode,
                             PripInsertMode.Y1))
        self.connect(self.pushButtonDatasetAdd,
                     QtCore.SIGNAL("clicked()"),
                     self.pushButtonDatasetAdd_clicked)
        self.connect(self.pushButtonDatasetRemove,
                     QtCore.SIGNAL("clicked()"),
                     self.pushButtonDatasetRemove_clicked)

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
        self.connect(self.actionExport_data_clipboard,
                        QtCore.SIGNAL("triggered()"),
                        self.model.export_data_clipboard)
        self.connect(self.actionExport_data_textfile,
                        QtCore.SIGNAL("triggered()"),
                        self.model.export_data_textfile)

        self.connect(self.listDatasets,
                        QtCore.SIGNAL("itemSelectionChanged()"),
                        self.selected_dataset_changed)

        # Mouse move
        self._graphicsScene.mouse_moved.connect(self.update_mouse_pos_status_bar)
        self._graphicsScene.mouse_pressed.connect(self.viewMousePressEvent)
        self._graphicsScene.point_item_moved.connect(self.point_item_moved)
        self._graphicsScene.axis_item_moved.connect(self.axis_item_moved)

    @QtCore.pyqtSlot(float, float)
    def update_mouse_pos_status_bar(self, x, y):
        coord = self.model.compute_coordinates([x,y])
        self.statusBar().showMessage("x=%f, y=%f" % tuple(coord))

    def new_project(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,
            'Select plot image to rip', path,
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tif)")
        if filename is not None and not str(filename) == "":
            # Clean previous state
            self.model.new_project(filename)
            self.view = PripView(self.model, self._graphicsScene, self.listDatasets)
            self.file_name = None
            self.update_interface()

    def open_project(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,
            'Select PRip project', path,
            "PRip project (*.prip)")
        if filename is not None and not str(filename) == "":
            # Try to load project
            self.model.load_project(filename)
            self.view = PripView(self.model, self._graphicsScene, self.listDatasets)
            self.file_name = filename
            self.update_interface()

    def save_project(self):
        if self.file_name is None:
            self.save_project_as()
        else:
            self.model.save_project(self.file_name)

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
            self.model.x0 = float(self.lineEditX0.text())
        except: pass
        try:
            self.model.x1 = float(self.lineEditX1.text())
        except: pass
        try:
            self.model.y0 = float(self.lineEditY0.text())
        except: pass
        try:
            self.model.y1 = float(self.lineEditY1.text())
        except: pass

    def update_interface(self):
        self.graphicsView.setEnabled(True)
        self.axesGroupPanel.setEnabled(True)
        self.datasetsGroupPanel.setEnabled(True)
        self.update_axis_references()

    def update_axis_references(self):
        self.lineEditX0.setText(str(self.model.x0))
        self.lineEditX1.setText(str(self.model.x1))
        self.lineEditY0.setText(str(self.model.y0))
        self.lineEditY1.setText(str(self.model.y1))

    def pushButtonDatasetAdd_clicked(self):
        self.model.add_dataset()

    def pushButtonDatasetRemove_clicked(self):
        row = self.listDatasets.currentRow()
        item = self.listDatasets.takeItem(row);
        self.model.remove_dataset(item._key)

        # self.listDatasets.setCurrentItem(item)
        # button = QtGui.QPushButton("hey");
        # item.setSizeHint(button.minimumSizeHint());
        # self.listDatasets.setItemWidget(item, button);
        # self.listDatasets.addItem("bar");

    def selected_dataset_changed(self):
        if not self.listDatasets.currentItem() is None:
            self.model.change_current_dataset(self.listDatasets.currentItem()._key)
        else:
            self.model.change_current_dataset(None)

    def viewMousePressEvent(self, event, item):
        mouse_pos = event.scenePos();
        mouse_pos = [mouse_pos.x(), mouse_pos.y()]
        mode = self.model.get_insert_mode()
        if event.button() == QtCore.Qt.LeftButton:
            if (item is None) or (item == self.view._background):
                if mode == PripInsertMode.Normal:
                    self.model.add_point(mouse_pos)
                else:
                    self.model.add_axis_ref(mouse_pos, mode)
                    self.model.set_insert_mode(PripInsertMode.Normal)
        elif event.button() == QtCore.Qt.RightButton:
            if (not item is None) and (item != self.view._background):
                if isinstance(item, PripGraphicsRectItem):
                    key = item.get_item_key()
                    self.model.remove_point(key)

    def point_item_moved(self, key, pos):
        self.model.move_point(key, [pos.x(), pos.y()])

    def axis_item_moved(self, key, pos):
        self.model.move_axis_ref(key, [pos.x(), pos.y()])


if __name__ == '__main__':
    # Entry point
    aplication = QtGui.QApplication(sys.argv)
    main_window = Main_Window(None)
    main_window.show()

    sys.exit(aplication.exec_())
