"""H_Snippet UI"""

from PySide2 import QtCore, QtGui, QtWidgets
import hou

from . import core

#


class SnippetTree(QtWidgets.QTreeWidget):
    """Snippet Tree custom Widget."""

    def __init__(self, *args, **kwargs):
        super(SnippetTree, self).__init__()
        self.snippet_folder = kwargs.pop("snippet_folder", None)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.setHeaderLabels(["Snippet Name", "From", "Date Received", "Path"])
        self.snippet_core = core.SnippetTreeCore()
        self.snippet_list = None
        self.set_snippet_list()
        self.fill_tree()
        self.setColumnHidden(3, True)

    def set_snippet_list(self):
        self.snippet_list = self.snippet_core.get_snippets_infos(self.snippet_folder)

    def fill_tree(self):
        for snippet in self.snippet_list:
            item = QtWidgets.QTreeWidgetItem(self)
            item.setText(0, snippet[0])
            item.setText(1, snippet[1])
            item.setText(2, snippet[2])
            item.setText(3, snippet[3])


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

        self.create_snippet_btn = QtWidgets.QPushButton("Create Snippet", self)
        self.send_snippet_btn = QtWidgets.QPushButton("Send Snippet to Clipboard", self)
        self.import_snippet_btn = QtWidgets.QPushButton(
            "Import Snippet from Clipboard", self
        )

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

        self.snippet = core.Snippet()
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

        # Appearance
        self.create_snippet_btn.setMaximumWidth(self.app_size[0] * 0.55)
        self.send_snippet_btn.setMaximumWidth(self.app_size[0] * 0.55)
        self.import_snippet_btn.setMaximumWidth(self.app_size[0] * 0.55)

        # UI Options
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setProperty("houdiniStyle", True)
        self.setStyleSheet(hou.ui.qtStyleSheet())

    def send_clipboard_to_snippet(self):
        """Get clipboard content and send it to snippet."""
        cb = QtGui.QGuiApplication.clipboard().text()
        self.snippet.import_snippet_from_clipboard(str(cb))

    def center_window(self):
        """Centers window on screen."""
        app_geo = self.frameGeometry()
        center_point = (
            QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        )
        app_geo.moveCenter(center_point)
        self.move(app_geo.topLeft())


def main():
    """UI main function."""
    main_window = hou.ui.mainQtWindow()
    for each in main_window.children():
        if each.objectName() == "mdev_H_snippet_main_window":
            return
    h_snippet = HSnippet()
    h_snippet.show()
