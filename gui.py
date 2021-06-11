import os
import sys
import math
import time
import shutil
import threading
from PyQt5 import QtCore, QtWidgets
from src.gui.styles import get_styles
from src.utils.datasets import Pagination
from src.utils.image_discovery import ImageDiscovery
from src.gui.worker_threads import TempProgressBarThread
from PyQt5.QtGui import QCursor, QPalette, QPainter, QBrush, QPen, QColor, QMovie
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QProgressBar
from PyQt5.QtWidgets import QStatusBar, QToolBar, QFrame, QGridLayout, QVBoxLayout, QFileDialog, QWidget, QLineEdit
from src.gui.event_handlers import open_folder, close_folder, exit_fn, temp, switch_tab, go_next, go_back, change_page, detect_faces, setup_empty_folder

# ---------------------------------------------------------------------------------------------
# ------------------------------------- Application State -------------------------------------
class ProgramState():

    def __init__(self, obj):
        self.current_tab = 1
        self.tab_pages = [1, 1, 1]
        self.active_tabs = [False, False, False]
        self.obj = obj

    def whereami(self):
        return self.current_tab, self.tab_pages[self.current_tab - 1]

    def change_page(self, new_page):
        self.tab_pages[self.current_tab - 1] = new_page

    def change_tab(self, tab):
        self.current_tab = tab
        print('Changed tab to {}'.format(self.current_tab))
        pg_section = self.obj.findChild(QFrame, 'pagination-section')
        if self.active_tabs[self.current_tab - 1]:
            pg_section.show()
        else:
            pg_section.hide()

    def activate_tab(self, tab):
        self.active_tabs[tab - 1] = True

    def deactivate_tab(self, tab):
        self.active_tabs[tab - 1] = False

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
    if objName == 'close-folder' or objName == 'find-faces' or objName == 'cluster-faces':
        wrapper.hide()
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
        self.program_state = ProgramState(self)
        self.imported_images = []
        self.selected_images = []
        self.selected_faces = []

    def create_first_paginator(self, files):
        self.pg1 = Pagination(files, page_size=15) 

    def create_second_paginator(self, files):
        self.pg2 = Pagination(files, page_size=15)

    def get_current_paginator(self):
        if self.program_state.whereami()[0] == 1:
            return self.pg1
        else:
            return self.pg2

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
                        ('./static/find-faces.svg', 'Find Faces', lambda: detect_faces(self), 'find-faces'),
                        ('./static/cluster-faces.svg', 'Cluster', lambda: print('fuck'), 'cluster-faces'), 
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
        progressbar_section.hide()

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
        tab_frame1_layout = QGridLayout()
        tab_frame1.setLayout(tab_frame1_layout)
        tab_frame2 = QFrame(objectName='tab-frame2')
        tab_frame2_layout = QGridLayout()
        tab_frame2.setLayout(tab_frame2_layout)
        tab_frame3 = QFrame(objectName='tab-frame3')
        tab_frame3_layout = QGridLayout()
        tab_frame3.setLayout(tab_frame3_layout)
        tab_frame2.hide()
        tab_frame3.hide()
        content_layout.addWidget(tab_head)
        content_layout.addWidget(tab_frame1)
        content_layout.addWidget(tab_frame2)
        content_layout.addWidget(tab_frame3)

        pagination = QFrame(objectName='pagination-section')
        pagination_layout = QHBoxLayout()
        pagination.setLayout(pagination_layout)
        pagination_layout.setContentsMargins(0, 0, 0, 0)
        prev_button = QPushButton('Previous Page', objectName='prev-btn')
        prev_button.clicked.connect(lambda: go_back(self))
        next_button = QPushButton('Next Page', objectName='next-btn')
        next_button.clicked.connect(lambda: go_next(self))
        prev_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        next_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        page_input = QLineEdit(objectName='page-input')
        page_input.returnPressed.connect(lambda: change_page(self, int(page_input.text())))
        page_input.setText('1')
        page_input.setAlignment(QtCore.Qt.AlignCenter)
        page_label = QLabel('/1000', objectName='page-label')
        pagination_layout.addWidget(prev_button)
        pagination_layout.addWidget(next_button)
        pagination_layout.addWidget(page_input)
        pagination_layout.addWidget(page_label)
        pagination.hide()

        main_section_layout.addWidget(progressbar_section)
        main_section_layout.addWidget(content)
        main_section_layout.addWidget(pagination)

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
