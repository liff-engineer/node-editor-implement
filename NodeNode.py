from collections import OrderedDict
from NodeSerializable import Serializable
from NodeGraphicsNode import QDMGraphicsNode
from NodeContentWidget import QDMNodeContentWidget
from NodeSocket import *


class Node(Serializable):
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        super().__init__()
        self.scene = scene

        self.title = title

        self.content = QDMNodeContentWidget(self)
        self.graphicsNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.graphicsScene.addItem(self.graphicsNode)

        self.socket_spacing = 22

        self.inputs = []
        self.outputs = []

        counter = 0

        for item in inputs:
            socket = Socket(self, counter, LEFT_BOTTOM, socket_type=item)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(self, counter, RIGHT_TOP, socket_type=item)
            counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.graphicsNode.pos()

    def setPos(self, x, y):
        self.graphicsNode.setPos(x, y)

    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)
                  ) else self.graphicsNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.graphicsNode.height - self.graphicsNode.edge_size - \
                self.graphicsNode._padding - index*self.socket_spacing
        else:
            y = self.graphicsNode.title_height+self.graphicsNode._padding + \
                self.graphicsNode.edge_size+index*self.socket_spacing

        return [x, y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def remove(self):
        for socket in (self.inputs + self.outputs):
            if socket.hasEdge():
                socket.edge.remove()

        self.scene.graphicsScene.removeItem(self.graphicsNode)
        self.scene.removeNode(self)

    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs:
            inputs.append(socket.serialize())

        for socket in self.outputs:
            outputs.append(socket.serialize())

        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.graphicsNode.scenePos().x()),
            ('pos_y', self.graphicsNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize())
        ])

    def deserialize(self, data, hashmap={}):
        return False
