import sys
import math
import time
import threading
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QCursor, QPalette, QPainter, QBrush, QPen, QColor, QMovie
from src.utils.image_discovery import ImageDiscovery
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QStatusBar, QToolBar, QFrame, QGridLayout, QVBoxLayout, QFileDialog, QWidget


# ------------------------------------------------------------------------------------------
# ------------------------------------- Event Handlers -------------------------------------

def open_folder(loading_section):
    folder = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
    def fn(loading_section):
        files = ImageDiscovery(folder_address=folder, save_folder='program_data').discover()
        time.sleep(1)
        loading_section.clear()
    add_animation(loading_section)
    threading.Thread(
        target=fn,
        args=(loading_section,)).start()

def temp():
    pass


# ---------------------------------------------------------------------------------------------
# ------------------------------------- Utility functions -------------------------------------

def create_button(icon_path, text, fn):
    wrapper = QFrame()
    wrapper_layout = QVBoxLayout()
    wrapper.setLayout(wrapper_layout)
    button = QPushButton()
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        """
        background-color: transparent;
        border-image: url({});
        """.format(icon_path)
    )
    button.clicked.connect(fn)
    wrapper.setStyleSheet(
        """
        * {
            max-width: 100px;
            max-height: 500px;
            margin: 0px;
            border: none;
            border-radius: 10px;
            background-color: white;
            height: 120px;
        }
        *:hover {
            background-color: #DDD;
        }
        """
    )
    label = QLabel(text)
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setStyleSheet(
        """
        background-color: transparent;
        """
    )
    wrapper_layout.addWidget(button, 1)
    wrapper_layout.addWidget(label, 2)
    return wrapper

def add_animation(wrapper):
    ani = QMovie('./static/loading-gif.gif')
    ani.setScaledSize(QtCore.QSize(80, 80))
    ani.frameChanged.connect(wrapper.repaint)
    wrapper.setMovie(ani)
    ani.start()
    return wrapper


# ------------------------------------------------------------------------------------
# ------------------------------------- Main GUI -------------------------------------
class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Clusterer')
        self.setFixedWidth(1500)
        self.setFixedHeight(700)
        self._createCentralWidget()

    def _createCentralWidget(self):
        main_frame = QFrame()
        grid = QGridLayout()
        main_frame.setLayout(grid)

        sidebar = QFrame()
        sidebar_grid = QVBoxLayout()
        sidebar.setLayout(sidebar_grid)
        sidebar.setStyleSheet(
            """
            margin: 10px;
            width: 100px;
            height: 300px;
            """
        )

        loading_section = QLabel()
        sidebar_grid.addWidget(
            create_button('./static/open-folder.png', 'Open Folder', lambda: open_folder(loading_section)), 1)
        sidebar_grid.addWidget(
            create_button('./static/find-faces.png', 'Find Faces', loading_section.clear), 2)
        sidebar_grid.addWidget(
            create_button('./static/find-faces.png', 'Temp Button', temp), 2)
        sidebar_grid.addWidget(
            create_button('./static/find-faces.png', 'Testing', temp), 2)
        sidebar_grid.addWidget(loading_section)

        content = QFrame()
        content.setStyleSheet(
            """
            margin: 10px;
            background-color: cyan;
            border: 2px solid red;
            """
        )
        # overlay.hide()

        grid.addWidget(sidebar, 0, 0)
        grid.addWidget(content, 0, 1, 1, 10)
        self.setCentralWidget(main_frame)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
