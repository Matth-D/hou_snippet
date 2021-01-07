"""H_Snippet UI"""

import os

from PySide2 import QtCore, QtGui, QtWidgets
import hou

from . import core


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
        self.selected_snippet = None
        self.setWindowFlags(QtCore.Qt.Tool)

    def init_ui(self):
        """Init UI Layout."""
        self.screen_size = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        self.app_size = (
            round(self.screen_size.width() * 0.35),
            round(self.screen_size.height() * 0.28),
        )
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.tab_widget = QtWidgets.QTabWidget()
        self.snippet_tab = QtWidgets.QWidget()
        self.library_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.snippet_tab, "Snippet")
        self.tab_widget.addTab(self.library_tab, "Library")
        self.snippet = core.Snippet()

        if self.snippet.is_internet:
            self.create_snippet_btn = QtWidgets.QPushButton("Create Snippet", self)
            self.send_snippet_btn = QtWidgets.QPushButton(
                "Send Snippet to Clipboard", self
            )
            self.import_snippet_btn = QtWidgets.QPushButton(
                "Import Snippet from Clipboard", self
            )
        self.no_internet_label = QtWidgets.QLabel(
            "Please connect your machine to the internet and restart H_snippet."
        )

        self.library_import_btn = QtWidgets.QPushButton("Import From Library", self)
        self.library_delete_btn = QtWidgets.QPushButton("Delete From Library", self)
        self.layout_v1 = QtWidgets.QVBoxLayout()
        self.layout_v1_h1 = QtWidgets.QHBoxLayout()
        self.layout_v1_h2 = QtWidgets.QHBoxLayout()
        self.layout_v1_h3 = QtWidgets.QHBoxLayout()
        self.layout_v2 = QtWidgets.QVBoxLayout()
        self.layout_h1 = QtWidgets.QHBoxLayout()

        # Don't draw buttons if GitTransfer and no internet
        if self.snippet.is_internet:
            self.layout_v1.addLayout(self.layout_v1_h1)
            self.layout_v1.addLayout(self.layout_v1_h2)
            self.layout_v1.addLayout(self.layout_v1_h3)

            self.layout_v1_h1.addWidget(self.create_snippet_btn)
            self.layout_v1_h2.addWidget(self.send_snippet_btn)
            self.layout_v1_h3.addWidget(self.import_snippet_btn)
        else:
            self.layout_v1.addWidget(self.no_internet_label)

        self.snippet_tab.setLayout(self.layout_v1)
        self.library_tab.setLayout(self.layout_v2)

        self.snippet_tree = SnippetTree(
            snippet_folder=self.snippet.snippet_received_path
        )
        self.layout_v2.addWidget(self.snippet_tree)
        self.layout_v2.addLayout(self.layout_h1)
        self.layout_h1.addWidget(self.library_import_btn)
        self.layout_h1.addWidget(self.library_delete_btn)

        self.main_layout.addWidget(self.tab_widget)

        # Signals and connect
        self.create_snippet_btn.clicked.connect(self.snippet.create_snippet_network)
        self.send_snippet_btn.clicked.connect(self.snippet.send_snippet_to_clipboard)
        self.import_snippet_btn.clicked.connect(self.send_clipboard_to_snippet)
        self.library_import_btn.clicked.connect(self.create_library_snippet)
        self.library_delete_btn.clicked.connect(self.remove_library_snippet)

        self.snippet_tree.itemClicked.connect(self.get_selected_snippet)

        # Appearance
        self.create_snippet_btn.setMaximumWidth(self.app_size[0] * 0.55)
        self.send_snippet_btn.setMaximumWidth(self.app_size[0] * 0.55)
        self.import_snippet_btn.setMaximumWidth(self.app_size[0] * 0.55)

        # UI Options
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setProperty("houdiniStyle", True)
        self.setStyleSheet(hou.ui.qtStyleSheet())

    def get_selected_snippet(self, item):
        """Update class variable with selected snippet in tree widget.

        Args:
            item (obj): QTreeWidgetItem object.
        """
        self.selected_snippet = str(item.data(3, 0))

    def create_library_snippet(self):
        """Create snippet network from local snippet file."""
        if not os.path.exists(self.selected_snippet):
            hou.ui.displayMessage("File is not present on disk.")
            return
        self.snippet.transfer.create_import_network(self.selected_snippet)

    def remove_library_snippet(self):
        """Delete selected snippet file in tree widget."""
        if not os.path.exists(self.selected_snippet):
            hou.ui.displayMessage("File is not present on disk.")
            return
        if hou.ui.displayConfirmation("Are you sure you want to delete this snippet ?"):
            os.remove(self.selected_snippet)
            self.snippet_tree.clear()
            self.snippet_tree.fill_tree()

    def send_clipboard_to_snippet(self):
        """Get clipboard content and send it to snippet."""
        clipboard = QtGui.QGuiApplication.clipboard().text()
        self.snippet.import_snippet_from_clipboard(str(clipboard))

    def center_window(self):
        """Centers window on screen."""
        app_geo = self.frameGeometry()
        center_point = (
            QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        )
        app_geo.moveCenter(center_point)
        self.move(app_geo.topLeft())


class SnippetTree(QtWidgets.QTreeWidget):
    """Snippet Tree custom Widget."""

    def __init__(self, *args, **kwargs):
        super(SnippetTree, self).__init__()
        self.snippet_folder = kwargs.pop("snippet_folder", None)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.setHeaderLabels(["Snippet Name", "From", "Date Received", "Path"])
        self.snippet_core = core.SnippetTreeCore()
        self.fill_tree()
        self.setColumnHidden(3, True)

    def fill_tree(self):
        """Fill H_snippet tree widget with snippet folder content."""

        snippet_list = self.snippet_core.get_snippets_infos(self.snippet_folder)
        for snippet in snippet_list:
            item = QtWidgets.QTreeWidgetItem(self)
            item.setText(0, snippet[0])
            item.setText(1, snippet[1])
            item.setText(2, snippet[2])
            item.setText(3, snippet[3])


def main():
    """UI main function."""
    main_window = hou.ui.mainQtWindow()
    for each in main_window.children():
        if each.objectName() == "mdev_H_snippet_main_window":
            return
    h_snippet = HSnippet()
    h_snippet.show()
