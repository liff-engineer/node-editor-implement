import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from nodeeditor.NodeScene import Scene
from nodeeditor.NodeNode import Node
from nodeeditor.NodeEdge import Edge, EDGE_TYPE_BEZIER
from nodeeditor.NodeGraphicsView import QDMGraphicsView


class NodeEditorAppView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.filename = None

        self.initUI()

    def initUI(self):
        #self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.scene = Scene()
        self.addNodes()

        self.view = QDMGraphicsView(self.scene.graphicsScene, self)
        self.layout.addWidget(self.view)

    def isModified(self):
        return self.scene.isModified()

    def isFilenameSet(self):
        return self.filename is not None

    def getSelectedItems(self):
        return self.scene.getSelectedItems()

    def hasSelectedItems(self):
        return self.getSelectedItems() != []

    def canUndo(self):
        return self.scene.history.canUndo()

    def canRedo(self):
        return self.scene.history.canRedo()

    def getUserFriendlyFilename(self):
        name = os.path.basename(
            self.filename) if self.isFilenameSet() else "NewGraph"
        return name + ("*" if self.isModified() else "")

    def fileNew(self):
        self.scene.clear()
        self.filename = None
        self.scene.history.clear()
        self.scene.history.storeInitialHistoryStamp()

    def fileLoad(self, filename):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.scene.loadFromFile(filename)
            self.filename = filename
            self.scene.history.clear()
            self.scene.history.storeInitialHistoryStamp()
            return True
        except InvalidFile as e:
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Error loading %s" %
                                os.path.basename(filename), str(e))
            return False
        finally:
            QApplication.restoreOverrideCursor()

    def fileSave(self, filename=None):
        # when called with empty parameter, we won't store the filename
        if filename is not None:
            self.filename = filename
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToFile(self.filename)
        QApplication.restoreOverrideCursor()
        return True

    def addNodes(self):
        node1 = Node(self.scene, "Awesome Node 1",
                     inputs=[0, 0, 0], outputs=[1])
        node2 = Node(self.scene, "Awesome Node 2",
                     inputs=[3, 3, 3], outputs=[1])
        node3 = Node(self.scene, "Awesome Node 3",
                     inputs=[2, 2, 2], outputs=[1])

        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge1 = Edge(
            self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(
            self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        self.scene.history.storeInitialHistoryStamp()

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.graphicsScene.addRect(-100, -
                                          100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.graphicsScene.addText(
            "This is my Awesome text !", QFont("微软雅黑"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.graphicsScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 100)

        # widget2 = QTextEdit()
        # proxy2 = self.graphicsScene.addWidget(widget2)
        # proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        # proxy2.setPos(0, 0)

        line = self.graphicsScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
        line.setFlag(QGraphicsItem.ItemIsMovable)

    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet.data(), encoding='utf-8'))
