import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QFileDialog, QFrame
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

def add_animation(wrapper):
    ani = QMovie('./static/loading-gif.gif')
    ani.setScaledSize(QtCore.QSize(80, 80))
    wrapper.setMovie(ani)
    ani.start()
    return wrapper
