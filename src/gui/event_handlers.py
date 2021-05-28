import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QFileDialog, QFrame, QPushButton
from src.gui.signal_handlers import update_progressbar, op_widget
from src.gui.worker_threads import TempProgressBarThread, ImageDiscoveryThread


def open_folder(obj, loading_section):
    folder = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
    if folder == '':
        return
    add_animation(loading_section)
    obj.t = ImageDiscoveryThread(obj, folder)
    obj.t.sig.connect(op_widget)
    obj.t.daemon = True
    obj.t.start()

def close_folder(obj):
    open_folder_button = obj.findChild(QFrame, 'open-folder')
    close_folder_button = obj.findChild(QFrame, 'close-folder')
    close_folder_button.hide()
    open_folder_button.show()

def exit_fn():
    sys.exit()

def temp(obj):
    obj.t = TempProgressBarThread(obj)
    obj.t.sig.connect(update_progressbar)
    obj.t.daemon = True
    obj.t.start()


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

def add_animation(wrapper):
    ani = QMovie('./static/loading-gif.gif')
    ani.setScaledSize(QtCore.QSize(80, 80))
    wrapper.setMovie(ani)
    ani.start()
    return wrapper
