
import time
from PyQt5 import QtCore
from src.utils.image_discovery import ImageDiscovery
from PyQt5.QtWidgets import QProgressBar, QFrame, QLabel, QMainWindow

class ImageDiscoveryThread(QtCore.QThread):

    sig = QtCore.pyqtSignal(QMainWindow, type, str, str)

    def __init__(self, obj, root, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.obj = obj
        self.root = root

    def run(self):
        files = ImageDiscovery(folder_address=self.root, save_folder='./program_data/paths').discover()
        time.sleep(1)
        self.sig.emit(self.obj, QFrame, 'open-folder', 'hide')
        self.sig.emit(self.obj, QFrame, 'close-folder', 'show')
        self.sig.emit(self.obj, QFrame, 'loading-section', 'clear')

class TempProgressBarThread(QtCore.QThread):

    sig = QtCore.pyqtSignal(QMainWindow, int)

    def __init__(self, obj, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.obj = obj

    def run(self):
        checkbox = self.obj.findChild(QProgressBar, "progressbar")
        start_value = checkbox.value()
        for i in range(start_value, 1000):
            time.sleep(0.1)
            self.sig.emit(self.obj, i)
