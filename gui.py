import os
import sys
import math
import time
import shutil
import threading
from PyQt5 import QtCore, QtWidgets
from src.utils.image_discovery import ImageDiscovery
from PyQt5.QtGui import QCursor, QPalette, QPainter, QBrush, QPen, QColor, QMovie
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

    # def __get_program_state(self):
    #     if not os.path.exists('./program_data'):
    #         os.mkdir('./program_data')
    #         return 'initial'
        
    #     if not os.path.exists('./program_data/paths'):
    #         if os.path.exists('./program_data/faces'):
    #             shutil.rmtree('./program_data/faces')
    #         if os.path.exists('./program_data/features'):
    #             shutil.rmtree('./program_data/features')
    #         if os.path.exists('./program_data/clusters'):
    #             shutil.rmtree('./program_data/clusters')
    #         return 'initial'

    #     if not os.path.exists('./program_data/faces'):
    #         if os.path.exists('./program_data/features'):
    #             shutil.rmtree('./program_data/features')
    #         if os.path.exists('./program_data/clusters'):
    #             shutil.rmtree('./program_data/clusters')
    #         return 'imported'
        
    #     if not os.path.exists('./program_data/features'):
    #         if os.path.exists('./program_data/clusters'):
    #             shutil.rmtree('./program_data/clusters')
    #         return 'detected'

    #     if not os.path.exists('./program_data/clusters'):
    #         return 'processed'

    #     return 'clustered'

# ----------------------------------------------------------------------------------
# ------------------------------------- Styles -------------------------------------

styles = """

#wholeWindow {
}

#sidebar {
    width: 100px;
    height: 300px;
}

#open-folder, #close-folder, #find-faces, #temp, #exit {
    max-width: 100px;
    max-height: 500px;
    margin: 0px;
    border: none;
    border-radius: 10px;
    background-color: rgb(41, 38, 100);
    height: 120px;
}
#close-folder, #exit {
    background-color: rgb(210, 0, 0);
}
#open-folder:hover, #find-faces:hover, #temp:hover {
    background-color: rgb(11, 8, 70);
}
#close-folder:hover, #exit:hover {
    background-color: rgb(140, 0, 0);
}
#open-folder-btn, #close-folder-btn, #find-faces-btn, #temp-btn, #exit-btn {
    height: 70px;
    background-color: transparent;
}
#open-folder-label, #close-folder-label, #find-faces-label, #temp-label, #exit-label {
    font-size: 15px;
    color: white;
    background-color: transparent;
}



#loading-section {
    padding-left: 10px;
}

#mainSection {
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

#btn-frame1, #btn-frame2, #btn-frame3 {
    background-color: rgb(210, 210, 210);
    height: 30px;
    font-size: 18px;
}
#btn-frame1 {
    color: white;
    background-color: rgb(41, 38, 100);
    border-top-left-radius: 10px;
    border-right: 1px solid rgb(178, 179, 180);
}
#btn-frame2 {
    border-radius: 0px;
    border-right: 1px solid rgb(178, 179, 180);
}
#btn-frame3 {
    border-top-right-radius: 10px;
}

#tab-frame1, #tab-frame2, #tab-frame3a {
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}

"""

# ------------------------------------------------------------------------------------------
# ------------------------------------- Event Handlers -------------------------------------

def open_folder(obj, loading_section):
    folder = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
    if folder == '':
        return
    add_animation(loading_section)
    threading.Thread(
        target=find_images,
        args=(obj, folder, loading_section)).start()

def close_folder(obj):
    open_folder_button = obj.findChild(QFrame, 'open-folder')
    close_folder_button = obj.findChild(QFrame, 'close-folder')
    close_folder_button.hide()
    open_folder_button.show()

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

def exit_fn():
    sys.exit()

# ---------------------------------------------------------------------------------------------
# ------------------------------------- Utility functions -------------------------------------


def find_images(obj, root, loading_section):
    files = ImageDiscovery(folder_address=root, save_folder='./program_data/paths').discover()
    open_folder_button = obj.findChild(QFrame, 'open-folder')
    close_folder_button = obj.findChild(QFrame, 'close-folder')
    time.sleep(1)
    open_folder_button.hide()
    close_folder_button.show()
    loading_section.clear()

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

def add_animation(wrapper):
    ani = QMovie('./static/loading-gif.gif')
    ani.setScaledSize(QtCore.QSize(80, 80))
    wrapper.setMovie(ani)
    ani.start()
    return wrapper

def switch_tab(obj, tab_number):
    def enable_btn(btn):
        btn.setStyleSheet("""
            color: white; 
            background-color: rgb(41, 38, 100);
        """)
    def disable_btn(btn):
        btn.setStyleSheet("""
            color: black; 
            background-color: rgb(210, 210, 210);
        """)

    btn1 = obj.findChild(QPushButton, "btn-frame1")
    btn2 = obj.findChild(QPushButton, "btn-frame2")
    btn3 = obj.findChild(QPushButton, "btn-frame3")
    tab1 = obj.findChild(QFrame, 'tab-frame1')
    tab2 = obj.findChild(QFrame, 'tab-frame2')
    tab3 = obj.findChild(QFrame, 'tab-frame3')

    if tab_number == 1: 
        enable_btn(btn1)
        disable_btn(btn2)
        disable_btn(btn3)
        tab1.show()
        tab2.hide()
        tab3.hide()

    elif tab_number == 2:
        disable_btn(btn1)
        enable_btn(btn2)
        disable_btn(btn3)
        tab1.hide()
        tab2.show()
        tab3.hide()

    elif tab_number == 3:
        disable_btn(btn1)
        disable_btn(btn2)
        enable_btn(btn3)
        tab1.hide()
        tab2.hide()
        tab3.show()

    obj.program_state.change_current_tab(tab_number)

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
    app.setStyleSheet(styles)
    win = Window()
    win.show()
    sys.exit(app.exec_())
