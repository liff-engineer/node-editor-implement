import json
from collections import OrderedDict
from nodeeditor.NodeSerializable import Serializable
from nodeeditor.NodeGraphicsScene import QDMGraphicsScene
from nodeeditor.NodeNode import Node
from nodeeditor.NodeEdge import Edge
from nodeeditor.NodeSceneHistory import SceneHistory
from nodeeditor.NodeSceneClipboard import SceneClipBoard


class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self._has_been_modified = False
        self._last_selected_items = []

        self._has_been_modified_listeners = []
        self._item_selected_listeners = []
        self._items_deselected_listeners = []

        self.initUI()

        self.history = SceneHistory(self)
        self.clipboard = SceneClipBoard(self)

        self.graphicsScene.itemSelected.connect(self.onItemSelected)
        self.graphicsScene.itemsDeselected.connect(self.onItemsDeselected)

    def onItemSelected(self):
        current_selected_items = self.getSelectedItems()
        if current_selected_items != self._last_selected_items:
            self._last_selected_items = current_selected_items
            self.history.storeHistory("Selection Changed")
            for callback in self._item_selected_listeners:
                callback()

    def onItemsDeselected(self):
        self.resetLastSelectedStates()
        if self._last_selected_items != []:
            self._last_selected_items = []
            self.history.storeHistory("Deselected Everything")
            for callback in self._items_deselected_listeners:
                callback()

    def isModified(self):
        return self.has_been_modified

    def getSelectedItems(self):
        return self.graphicsScene.selectedItems()

    @property
    def has_been_modified(self):
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value

    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def initUI(self):
        self.graphicsScene = QDMGraphicsScene(self)
        self.graphicsScene.setGraphicsScene(
            self.scene_width, self.scene_height)

    def addItemSelectedListener(self, callback):
        self._item_selected_listeners.append(callback)

    def addItemsDeselectedListener(self, callback):
        self._items_deselected_listeners.append(callback)

    # custom flag to detect node or edge has been selected....

    def resetLastSelectedStates(self):
        for node in self.nodes:
            node.graphicsNode._last_selected_state = False
        for edge in self.edges:
            edge.graphicsEdge._last_selected_state = False

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
        else:
            print("!W:", "Scene::removeNode", "wanna remove node",
                  node, "from self.nodes but it's not in the list!")

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print("!W:", "Scene::removeEdge", "wanna remove edge",
                  edge, "from self.edges but it's not in the list!")

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

        self.has_been_modified = False

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
        print("saving to", filename, "was successfull.")

        self.has_been_modified = False

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)

            self.has_been_modified = False

    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes:
            nodes.append(node.serialize())
        for edge in self.edges:
            edges.append(edge.serialize())

        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        print("deserializating data", data)

        self.clear()
        hashmap = {}

        if restore_id:
            self.id = data['id']

        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap, restore_id)
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)
        return True
