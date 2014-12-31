# Prip
# class PripGraphicsScene

from PyQt4 import QtCore, QtGui, uic

from vector import *
import pickle

class PripGraphicsScene(QtGui.QGraphicsScene):

    class InsertMode:
        Normal, X0, X1, Y0, Y1 = range(5)

    # Signal emitted when the mouse is moved
    mouse_moved = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)
        self.reset()

    def reset(self):
        self.clear()

        self._background_file = None
        self._background = None

        self._axis_refs = {}
        self._points = []
        self._mode = PripGraphicsScene.InsertMode.Normal

        self.x0 = 0.0
        self.x1 = 1.0
        self.y0 = 0.0
        self.y1 = 1.0

    def new_project(self, background_file = None):
        self.reset()
        if not background_file is None:
            self.add_image(background_file)

    def save_project(self, project_file):
        # Construct dict to dump
        d = {}
        d["background_file"] = str(self._background_file)
        d["x0"] = self.x0
        d["x1"] = self.x1
        d["y0"] = self.y0
        d["y1"] = self.y1

        # Convert axis refs items to coordinates
        axis_refs = {}
        for key in self._axis_refs:
            if self._axis_refs[key] is None:
                axis_refs[key] = None
            else:
                axis_refs[key] = self._axis_refs[key].scenePos()
        d["axis_refs"] = axis_refs

        # Convert items to coordinates
        points = []
        for p in self._points:
            points.append(p.scenePos())
        d["points"] = points

        try:
            oF = open(project_file, 'wb')
            pickle.dump("PripV0.1", oF)
            pickle.dump(d, oF)
            oF.close()
            return True
        except:
            return False

    def load_project(self, project_file):
        self.reset()

        with open(project_file, 'rb') as iF:
            header = pickle.load(iF)
            if header == "PripV0.1":
                d = pickle.load(iF)

                def assignIfExists(var, d, keyname):
                    if keyname in d:
                        return d[keyname]
                    else:
                        return var

                background_file = d["background_file"]
                self.add_image(background_file)
                self.x0 = assignIfExists(self.x0, d, "x0")
                self.x1 = assignIfExists(self.x1, d, "x1")
                self.y0 = assignIfExists(self.y0, d, "y0")
                self.y1 = assignIfExists(self.y1, d, "y1")

                for key in d["axis_refs"]:
                    if not d["axis_refs"][key] is None:
                        self.add_axis_ref(d["axis_refs"][key], key)

                for p in d["points"]:
                    self.add_point(p)

                return True
            else:
                return False
        return False

    def add_image(self, background_file):
        pixmap = QtGui.QPixmap(background_file)
        self._background_file = background_file
        self._background = self.addPixmap(pixmap)

    def set_insert_mode(self, mode):
        self._mode = mode

    def add_point(self, pos):
        item = self.addRect(-5.0, -5.0, 10.0, 10.0)
        item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        item.setPos(pos);

        self._points.append(item)

    def remove_point(self, item):
        if item in self._points:
            self.removeItem(item)
            self._points.remove(item)

    def add_axis_ref(self, pos, mode):
        if mode in self._axis_refs:
            if not self._axis_refs[mode] is None:
                self.removeItem(self._axis_refs[mode])

        item = self.addEllipse(-5.0, -5.0, 10.0, 10.0)
        item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        item.setPos(pos);
        self._axis_refs[mode] = item

    def mousePressEvent(self, event):
        mouse_pos = event.scenePos();
        item = self.itemAt(mouse_pos)

        if event.button() == QtCore.Qt.LeftButton:
            if (item is None) or (item == self._background):
                if self._mode == PripGraphicsScene.InsertMode.Normal:
                    self.add_point(mouse_pos)
                else:

                    self.add_axis_ref(mouse_pos, self._mode)
                    self._mode = PripGraphicsScene.InsertMode.Normal

        elif event.button() == QtCore.Qt.RightButton:
            if (not item is None) and (item != self._background):
                self.remove_point(item)

        QtGui.QGraphicsScene.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsScene.mouseMoveEvent(self, event)

        if not PripGraphicsScene.InsertMode.X0 in self._axis_refs:
            return
        if not PripGraphicsScene.InsertMode.X1 in self._axis_refs:
            return
        if not PripGraphicsScene.InsertMode.Y0 in self._axis_refs:
            return
        if not PripGraphicsScene.InsertMode.Y1 in self._axis_refs:
            return
        coords = self.compute_coordinates(event.scenePos())
        self.mouse_moved.emit(coords[0], coords[1])

    def compute_coordinates(self, pos):
        coord = [0,0]
        x0Pos = self._axis_refs[PripGraphicsScene.InsertMode.X0].scenePos()
        x1Pos = self._axis_refs[PripGraphicsScene.InsertMode.X1].scenePos()
        y0Pos = self._axis_refs[PripGraphicsScene.InsertMode.Y0].scenePos()
        y1Pos = self._axis_refs[PripGraphicsScene.InsertMode.Y1].scenePos()

        # Find projecting over x axis
        A = [[x1Pos.x() - x0Pos.x(),
              x1Pos.y() - x0Pos.y()],
             [y1Pos.x() - y0Pos.x(),
              y1Pos.y() - y0Pos.y()]]

        b = [pos.x() - x0Pos.x(),
             pos.y() - x0Pos.y()]

        [alpha, beta] = solve_linear_2x2(A, b)
        coord[0] = self.x0 + (self.x1 - self.x0) * alpha

        # Find projecting over y axis
        b = [pos.x() - y0Pos.x(),
             pos.y() - y0Pos.y()]

        [alpha, beta] = solve_linear_2x2(A, b)
        coord[1] = self.y0 + (self.y1 - self.y0) * beta

        return coord
