import sys
from PySide2.QtWidgets import *
from nodeeditor.NodeEditor import NodeEditor

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # label = QLabel("Hello, PySide2!")
    # label.show()
    appView = NodeEditor()
    appView.show()
    sys.exit(app.exec_())
