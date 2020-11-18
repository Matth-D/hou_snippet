"""H_Snippet UI"""

import hou
from PySide2 import QtWidgets, QtGui, QtCore


class HSnippet(QtWidgets.QDialog):
    """H_Snippet UI main class.

    Args:
        QtWidgets (class): QtWidgets.QDialog inheritance.
    """

    def __init__(self):
        super(HSnippet, self).__init__()
        self.init_ui()
        self.setGeometry(300, 300, self.app_size[0], self.app_size[1])
        self.center_window()
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

    def init_ui(self):
        """Init UI Layout."""
        self.screen_size = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        self.app_size = (
            round(self.screen_size.width() * 0.25),
            round(self.screen_size.height() * 0.2),
        )
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.button1 = QtWidgets.QPushButton("Button1", self)
        self.button2 = QtWidgets.QPushButton("Button2", self)
        self.button3 = QtWidgets.QPushButton("Button3", self)

        self.main_layout.addWidget(self.button1)
        self.main_layout.addWidget(self.button2)
        self.main_layout.addWidget(self.button3)

        # UI Options
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setProperty("houdiniStyle", True)
        self.setStyleSheet(hou.ui.qtStyleSheet())

    def center_window(self):
        """Centers window on screen."""

        app_geo = self.frameGeometry()
        center_point = (
            QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        )
        app_geo.moveCenter(center_point)
        self.move(app_geo.topLeft())

    # def closeEvent(self, event):
    #     print "attempt to close window"
    #     print event


# TODO: write closeEvent method to clean window when closed.
def main():
    h_snippet = HSnippet()
    h_snippet.show()