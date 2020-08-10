import sys
from PySide2.QtWidgets import *
from NodeEditorAppView import NodeEditorAppView

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # label = QLabel("Hello, PySide2!")
    # label.show()
    appView = NodeEditorAppView()
    appView.show()
    sys.exit(app.exec_())
