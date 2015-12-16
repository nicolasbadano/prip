# Prip
# class PripView
from PyQt4 import QtCore, QtGui, uic
from PripInsertMode import PripInsertMode
from PripGraphicsRectItem import PripGraphicsRectItem
from PripGraphicsAxisItem import PripGraphicsAxisItem

from vector import *
import pickle

class PripView:

    class Helpers:
        LineX, LineY = range(2)

    class Preferences:
        Pen_Axis_ref_X = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine,
                                    QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin);
        Pen_Axis_ref_Y = QtGui.QPen(QtCore.Qt.blue, 2, QtCore.Qt.SolidLine,
                                    QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin);
        Pen_Axis_line_X = QtGui.QPen(QtCore.Qt.red, 1.2, QtCore.Qt.SolidLine,
                                     QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin);
        Pen_Axis_line_Y = QtGui.QPen(QtCore.Qt.blue, 1.2, QtCore.Qt.SolidLine,
                                     QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin);
        Pen_Point = QtGui.QPen(QtCore.Qt.green, 2, QtCore.Qt.SolidLine,
                               QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin);

    def __init__(self, model, graphicScene):
        self._model = model
        self._graphicScene = graphicScene

        self.reset()
        self._model.model_changed.connect(self.model_changed)
        self.model_changed()

    def reset(self):
        self._graphicScene.clear()

        background_file = self._model.get_background_file()
        pixmap = QtGui.QPixmap(background_file)
        self._background = self._graphicScene.addPixmap(pixmap)

        self._axis_ref_items = {}
        self._axis_line_items = {}
        self._point_items = {}

        self._current_dataset = None

    def model_changed(self):
        self.update_point_items()
        self.update_axis_refs()

    def update_point_items(self):
        model_points = self._model.get_points()
        set_model_keys = set(model_points.keys())
        set_view_keys = set(self._point_items.keys())
        set_intersect_keys = set_model_keys.intersection(set_view_keys)
        # Added points
        added_keys = set_model_keys - set_intersect_keys
        for key in added_keys:
            pos, dataset = model_points[key]
            pos = QtCore.QPointF(pos[0], pos[1])
            self.add_point_item(key, pos, dataset)

        # Removed points
        removed_keys = set_view_keys - set_intersect_keys
        for key in removed_keys:
            self.remove_point_item(key)

        # Potentially moved points
        for key in set_intersect_keys:
            model_pos = model_points[key][0]
            model_pos = QtCore.QPointF(model_pos[0], model_pos[1])
            item = self._point_items[key][0]
            dist = (model_pos - item.scenePos()).manhattanLength()
            if dist > 0.001:
                item.setPos(model_pos)

    def add_point_item(self, key, pos, dataset):
        item = PripGraphicsRectItem(PripView.Preferences.Pen_Point, key)
        self._point_items[key] = (item, dataset)
        self._graphicScene.addItem(item)
        item.setPos(pos);

    def remove_point_item(self, key):
        item, dataset = self._point_items[key]
        self._graphicScene.removeItem(item)
        del self._point_items[key]

    def update_axis_refs(self):
        model_refs = self._model.get_axis_refs()
        set_model_keys = set(model_refs.keys())
        set_view_keys = set(self._axis_ref_items.keys())
        set_intersect_keys = set_model_keys.intersection(set_view_keys)

        # Added refs
        added_keys = set_model_keys - set_intersect_keys
        for key in added_keys:
            pos = model_refs[key]
            pos = QtCore.QPointF(pos[0], pos[1])
            self.add_axis_ref(pos, key)

        # Removed refs
        removed_keys = set_view_keys - set_intersect_keys
        for key in removed_keys:
            self.remove_axis_ref(key)

        # Potentially moved refs
        for key in set_intersect_keys:
            model_pos = model_refs[key]
            model_pos = QtCore.QPointF(model_pos[0], model_pos[1])
            item = self._axis_ref_items[key]
            dist = (model_pos - item.scenePos()).manhattanLength()
            if dist > 0.001:
                item.setPos(model_pos)

        self.update_axis_lines()

    def add_axis_ref(self, pos, mode):
        pen = PripView.Preferences.Pen_Axis_ref_X
        if mode == PripInsertMode.Y0 or \
           mode == PripInsertMode.Y1:
            pen = PripView.Preferences.Pen_Axis_ref_Y

        item = PripGraphicsAxisItem(pen, mode)
        self._axis_ref_items[mode] = item
        self._graphicScene.addItem(item)
        item.setPos(pos);

    def remove_axis_ref(self, mode):
        self._graphicScene.removeItem(self._axis_ref_items)
        del self._graphicScene._axis_ref_items[mode]

    def update_axis_lines(self):
        if PripInsertMode.X0 in self._axis_ref_items and \
           PripInsertMode.X1 in self._axis_ref_items:
            line = QtCore.QLineF(self._axis_ref_items[PripInsertMode.X0].scenePos(),
                                 self._axis_ref_items[PripInsertMode.X1].scenePos())
            if not PripView.Helpers.LineX in self._axis_line_items:
                pen = PripView.Preferences.Pen_Axis_line_X
                item = self._graphicScene.addLine(line, pen)
                item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
                self._axis_line_items[PripView.Helpers.LineX] = item
            else:
                self._axis_line_items[PripView.Helpers.LineX].setLine(line)

        if PripInsertMode.Y0 in self._axis_ref_items and \
           PripInsertMode.Y1 in self._axis_ref_items:
            line = QtCore.QLineF(self._axis_ref_items[PripInsertMode.Y0].scenePos(),
                                 self._axis_ref_items[PripInsertMode.Y1].scenePos())
            if not PripView.Helpers.LineY in self._axis_line_items:
                pen = PripView.Preferences.Pen_Axis_line_Y
                item = self._graphicScene.addLine(line, pen)
                item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
                self._axis_line_items[PripView.Helpers.LineY] = item
            else:
                self._axis_line_items[PripView.Helpers.LineY].setLine(line)
