import sys
import math
import time
import threading
from PyQt5 import QtCore, QtWidgets
from src.utils.image_discovery import ImageDiscovery
from PyQt5.QtGui import QCursor, QPalette, QPainter, QBrush, QPen, QColor, QMovie
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QProgressBar
from PyQt5.QtWidgets import QStatusBar, QToolBar, QFrame, QGridLayout, QVBoxLayout, QFileDialog, QWidget

# ----------------------------------------------------------------------------------
# ------------------------------------- Styles -------------------------------------

styles = """

#sidebar {
    margin: 10px;
    width: 100px;
    height: 300px;
}

#progressbar {
    color: white;
    font-size: 18px;
    text-align: center;
    max-height: 20px;
    background-color: rgb(178, 179, 180);
    border-radius: 10px;
}
#progressbar::chunk {
    background-color: rgb(41, 38, 100);
    border-radius: 8px;
}

#content {
    background-color: white;
    border-radius: 10px;
}

#tab-head {
    max-height: 30px;
}

#btn-frame1, #btn-frame2 {
    border: 0px;
    background-color: rgb(210, 210, 210);
    height: 30px;
    font-size: 18px;
}
#btn-frame1:hover, #btn-frame2:hover {
    color: white;
    background-color: rgb(41, 38, 100);
}
#btn-frame1 {
    border-top-left-radius: 10px;
}
#btn-frame2 {
    border-top-right-radius: 10px;
}

"""

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

def temp(obj):
    def fn():
        checkbox = obj.findChild(QProgressBar, "progressbar")
        start_value = checkbox.value()
        for i in range(start_value, 1000):
            time.sleep(0.1)
            checkbox.setValue(i)
            checkbox.repaint()
    
    threading.Thread(
        target=fn
    ).start()

def exit():
    exit()


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

        # Sidebar
        sidebar = QFrame(objectName='sidebar')
        sidebar_grid = QVBoxLayout()
        sidebar.setLayout(sidebar_grid)
        loading_section = QLabel()
        buttons_info = [('./static/open-folder.png', 'Open Folder', lambda: open_folder(loading_section)),
                       ('./static/find-faces.png', 'Find Faces', loading_section.clear),
                       ('./static/find-faces.png', 'Temp Button', lambda: temp(self)), 
                       ('./static/find-faces.png', 'Exit', exit)]
        for path, title, fn in buttons_info:
            sidebar_grid.addWidget(create_button(path, title, fn))
        sidebar_grid.addWidget(loading_section)

        # Main section
        main_section = QFrame()
        main_section_layout = QVBoxLayout()
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
        button_frame1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button_frame2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        tab_head_layout.addWidget(button_frame1)
        tab_head_layout.addWidget(button_frame2)
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
    app = QApplication(sys.argv)
    app.setStyleSheet(styles)
    win = Window()
    win.show()
    sys.exit(app.exec_())
