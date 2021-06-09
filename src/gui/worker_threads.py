import time
import itertools
from typing import NewType
import numpy as np
from PyQt5 import QtCore
from src.utils.detection import Detection
from src.utils.image_discovery import ImageDiscovery
from PyQt5.QtWidgets import QProgressBar, QFrame, QLabel, QMainWindow, QGridLayout

class ImageDiscoveryThread(QtCore.QThread):

    sig = QtCore.pyqtSignal(QMainWindow, type, str, str)
    finish = QtCore.pyqtSignal(QMainWindow, list)

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
        self.finish.emit(self.obj, files)

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

class FaceDetectionThread(QtCore.QThread):
    
    sig = QtCore.pyqtSignal(QMainWindow, int)
    finish = QtCore.pyqtSignal(QMainWindow, list)
    
    def __init__(self, obj, csv_files, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.obj = obj
        self.csv_files = csv_files

    def run(self):
        progressbar = self.obj.findChild(QProgressBar, "progressbar")
        det = Detection(self.csv_files, './program_data/faces', 32, (250, 250), device='cuda:0', same=False)
        face_files = det.detect_faces(num_workers=2, gui_params=(self.obj, self.sig))
        self.finish.emit(self.obj, face_files)

# class PrepareImageThread(QtCore.QThread):

#     sig = QtCore.pyqtSignal(QGridLayout, int, int)

#     def __init__(self, obj, csv_file, page_num, type=1, batch_size=9, parent=None):
#         QtCore.QThread.__init__(self, parent)
#         self.csv_file = csv_file
#         self.page_num = page_num
#         self.type = type
#         self.obj = obj

#     def run(self):
#         if type == 1:
#             self.read_images()
#         elif type == 2:
#             self.read_faces()

#     def read_images(self):


#         beginning = (self.page_num - 1) * self.batch_size


#     def read_faces(self):
#         pass
