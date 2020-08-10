from collections import OrderedDict
from NodeSerializable import Serializable
from NodeGraphicsEdge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = False


class Edge(Serializable):
    def __init__(self, scene, start_socket, end_socket, edge_type=EDGE_TYPE_DIRECT):
        super().__init__()
        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.graphicsEdge = QDMGraphicsEdgeDirect(
            self) if edge_type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.updatePositions()

        self.scene.graphicsScene.addItem(self.graphicsEdge)
        self.scene.addEdge(self)

    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.graphicsNode.pos().x()
        source_pos[1] += self.start_socket.node.graphicsNode.pos().y()
        self.graphicsEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.graphicsNode.pos().x()
            end_pos[1] += self.end_socket.node.graphicsNode.pos().y()
            self.graphicsEdge.setDestination(*end_pos)
        else:
            self.graphicsEdge.setDestination(*source_pos)
        self.graphicsEdge.update()

    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        if DEBUG:
            print("# Removing Edge", self)
            print("- remove edge from all sockets")
        self.remove_from_sockets()
        self.scene.graphicsScene.removeItem(self.graphicsEdge)
        self.graphicsEdge = None
        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass

        if DEBUG:
            print("- everything is done.")

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('edge_type', self.edge_type),
            ('start', self.start_socket.id),
            ('end', self.end_socket.id),
        ])

    def deserialize(self, data, hashmap={}):
        return False
