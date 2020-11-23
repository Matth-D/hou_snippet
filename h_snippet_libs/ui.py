"""H_Snippet UI"""

from PySide2 import QtCore, QtGui, QtWidgets

import hou

from . import core


class SnippetTree(QtWidgets.QTreeWidget):
    """Snippet Tree custom Widget."""

    def __init__(self, *args, **kwargs):
        super(SnippetTree, self).__init__()
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.setHeaderLabels(["Snippet Name", "From", "Date Received"])


class HSnippet(QtWidgets.QDialog):
    """H_Snippet UI main class"""

    def __init__(self):
        super(HSnippet, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setObjectName("mdev_H_snippet_main_window")
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

        self.tab_widget = QtWidgets.QTabWidget()
        self.snippet_tab = QtWidgets.QWidget()
        self.library_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.snippet_tab, "Snippet")
        self.tab_widget.addTab(self.library_tab, "Library")

        self.create_snippet_btn = QtWidgets.QPushButton("Create Snippet", self)
        self.send_snippet_btn = QtWidgets.QPushButton("Send Snippet to Clipboard", self)
        self.import_snippet_btn = QtWidgets.QPushButton(
            "Import Snippet from Clipboard", self
        )

        self.snippet_tree = SnippetTree()
        self.library_import_btn = QtWidgets.QPushButton("Import From Library", self)
        self.library_delete_btn = QtWidgets.QPushButton("Delete From Library", self)
        self.layout_v1 = QtWidgets.QVBoxLayout()
        self.layout_v1_h1 = QtWidgets.QHBoxLayout()
        self.layout_v1_h2 = QtWidgets.QHBoxLayout()
        self.layout_v1_h3 = QtWidgets.QHBoxLayout()
        self.layout_v2 = QtWidgets.QVBoxLayout()
        self.layout_h1 = QtWidgets.QHBoxLayout()

        self.layout_v1.addLayout(self.layout_v1_h1)
        self.layout_v1.addLayout(self.layout_v1_h2)
        self.layout_v1.addLayout(self.layout_v1_h3)

        self.layout_v1_h1.addWidget(self.create_snippet_btn)
        self.layout_v1_h2.addWidget(self.send_snippet_btn)
        self.layout_v1_h3.addWidget(self.import_snippet_btn)

        self.snippet_tab.setLayout(self.layout_v1)
        self.library_tab.setLayout(self.layout_v2)

        self.layout_v2.addWidget(self.snippet_tree)
        self.layout_v2.addLayout(self.layout_h1)
        self.layout_h1.addWidget(self.library_import_btn)
        self.layout_h1.addWidget(self.library_delete_btn)

        self.main_layout.addWidget(self.tab_widget)

        # self.test_class = core.classTest()
        self.snippet = core.Snippet()

        # Signals and connect
        self.create_snippet_btn.clicked.connect(self.snippet.create_snippet_network)
        self.send_snippet_btn.clicked.connect(self.snippet.send_snippet_to_clipboard)
        # self.send_snippet_btn.clicked.connect(self.test_class.print_selection)

        # Appearance
        self.create_snippet_btn.setMaximumWidth(self.app_size[0] * 0.55)
        self.send_snippet_btn.setMaximumWidth(self.app_size[0] * 0.55)
        self.import_snippet_btn.setMaximumWidth(self.app_size[0] * 0.55)
        # self.library_import_btn.setMaximumWidth(self.app_size[0] * 0.3)
        # self.library_delete_btn.setMaximumWidth(self.app_size[0] * 0.3)

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


def main():
    main_window = hou.ui.mainQtWindow()
    for each in main_window.children():
        if each.objectName() == "mdev_H_snippet_main_window":
            return
    h_snippet = HSnippet()
    h_snippet.show()
