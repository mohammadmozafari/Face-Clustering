import os
import sys
import math
import time
import shutil
import threading
from PyQt5 import QtCore, QtWidgets
from src.gui.styles import get_styles
from src.utils.image_discovery import ImageDiscovery
from src.gui.worker_threads import TempProgressBarThread
from PyQt5.QtGui import QCursor, QPalette, QPainter, QBrush, QPen, QColor, QMovie
from src.gui.event_handlers import open_folder, close_folder, exit_fn, temp, switch_tab
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QProgressBar
from PyQt5.QtWidgets import QStatusBar, QToolBar, QFrame, QGridLayout, QVBoxLayout, QFileDialog, QWidget

# ---------------------------------------------------------------------------------------------
# ------------------------------------- Application State -------------------------------------
class ProgramState():

    def __init__(self, obj):
        self.current_tab = 1
        self.state = 'initial'
        self.obj = obj

    def change_current_tab(self, tab):
        self.current_tab = tab
        print('Changed tab to {}'.format(self.current_tab))

# ---------------------------------------------------------------------------------------------
# ------------------------------------- Utility functions -------------------------------------

def create_button(icon_path, text, fn, objName):
    wrapper = QFrame(objectName=objName)
    wrapper_layout = QVBoxLayout()
    wrapper.setLayout(wrapper_layout)
    button = QPushButton(objectName='{}-btn'.format(objName))
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        """
        border-image: url({});
        """.format(icon_path)
    )
    button.clicked.connect(fn)
    label = QLabel(text, objectName='{}-label'.format(objName))
    label.setAlignment(QtCore.Qt.AlignCenter)
    wrapper_layout.addWidget(button, 1)
    wrapper_layout.addWidget(label, 2)
    if objName == 'close-folder':
        wrapper.hide()
    return wrapper

def setup_empty_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)
        return
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# ------------------------------------------------------------------------------------
# ------------------------------------- Main GUI -------------------------------------
class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Clusterer')
        self.setFixedWidth(1500)
        self.setFixedHeight(700)
        self._createCentralWidget()
        self.program_state = ProgramState(self)

    def _createCentralWidget(self):
        main_frame = QFrame(objectName='wholeWindow')
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(20)
        main_frame.setLayout(grid)

        # Sidebar
        sidebar = QFrame(objectName='sidebar')
        sidebar_grid = QVBoxLayout()
        sidebar_grid.setContentsMargins(40, 20, 0, 40)
        sidebar.setLayout(sidebar_grid)
        loading_section = QLabel(objectName='loading-section')
        buttons_info = [('./static/open-folder.svg', 'Open Folder', lambda: open_folder(self, loading_section), 'open-folder'),
                        ('./static/close-folder.svg', 'Close Folder', lambda: close_folder(self), 'close-folder'),
                        ('./static/find-faces.svg', 'Find Faces', loading_section.clear, 'find-faces'),
                        ('./static/find-faces.svg', 'Temp Button', lambda: temp(self), 'temp'), 
                        ('./static/find-faces.svg', 'Exit', exit_fn, 'exit')]
        for path, title, fn, objName in buttons_info:
            sidebar_grid.addWidget(create_button(path, title, fn, objName))
        sidebar_grid.addWidget(loading_section)

        # Main section
        main_section = QFrame(objectName='mainSection')
        main_section_layout = QVBoxLayout()
        main_section_layout.setContentsMargins(0, 20, 40, 0)
        main_section.setLayout(main_section_layout)
        progressbar_section = QProgressBar(minimum=0, maximum=1000, objectName='progressbar')
        progressbar_section.setValue(13)

        content = QFrame(objectName='content')
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content.setLayout(content_layout)
        tab_head = QFrame(objectName='tab-head')
        tab_head_layout = QHBoxLayout()
        tab_head.setLayout(tab_head_layout)
        tab_head_layout.setContentsMargins(0, 0, 0, 0)
        tab_head_layout.setSpacing(0)
        button_frame1 = QPushButton('Imported Images', objectName='btn-frame1')
        button_frame2 = QPushButton('Detected Faces', objectName='btn-frame2')
        button_frame3 = QPushButton('People', objectName='btn-frame3')
        button_frame1.clicked.connect(lambda: switch_tab(self, 1))
        button_frame2.clicked.connect(lambda: switch_tab(self, 2))
        button_frame3.clicked.connect(lambda: switch_tab(self, 3))
        button_frame1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button_frame2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button_frame3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        tab_head_layout.addWidget(button_frame1)
        tab_head_layout.addWidget(button_frame2)
        tab_head_layout.addWidget(button_frame3)
        tab_frame1 = QFrame(objectName='tab-frame1')
        tab_frame2 = QFrame(objectName='tab-frame2')
        tab_frame3 = QFrame(objectName='tab-frame3')
        tab_frame2.hide()
        tab_frame3.hide()
        content_layout.addWidget(tab_head)
        content_layout.addWidget(tab_frame1)
        content_layout.addWidget(tab_frame2)
        content_layout.addWidget(tab_frame3)
        main_section_layout.addWidget(progressbar_section)
        main_section_layout.addWidget(content)

        grid.addWidget(sidebar, 0, 0)
        grid.addWidget(main_section, 0, 1, 1, 10)
        self.setCentralWidget(main_frame)

if __name__ == '__main__':
    setup_empty_folder('./program_data')
    app = QApplication(sys.argv)
    app.setStyleSheet(get_styles())
    win = Window()
    win.show()
    sys.exit(app.exec_())
