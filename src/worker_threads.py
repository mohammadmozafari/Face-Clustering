import time
import torch
import itertools
import numpy as np
from PyQt5 import QtCore
import s0_discover_images
from typing import NewType
from detection import MTCNNDetection
from clustering import cluster_faces
from utils.feature_extraction import FeatureExtractor
from PyQt5.QtWidgets import QProgressBar, QFrame, QLabel, QMainWindow, QGridLayout
from utils import save_images_with_bboxes

class ImageDiscoveryThread(QtCore.QThread):

    sig = QtCore.pyqtSignal(QMainWindow, type, str, str)
    finish = QtCore.pyqtSignal(QMainWindow, list)

    def __init__(self, obj, root, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.obj = obj
        self.root = root

    def run(self):
        files = s0_discover_images.main(self.root, './data/program_data')
        time.sleep(1)
        self.sig.emit(self.obj, QFrame, 'open-folder', 'hide')
        self.sig.emit(self.obj, QFrame, 'close-folder', 'show')
        self.sig.emit(self.obj, QFrame, 'loading-section', 'clear')
        self.sig.emit(self.obj, QFrame, 'find-faces', 'show')
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
    
    pbar_sig = QtCore.pyqtSignal(QMainWindow, int)
    finish = QtCore.pyqtSignal(QMainWindow, list)
    show_sig = QtCore.pyqtSignal(QMainWindow, type, str, str)
    
    def __init__(self, obj, csv_files, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.obj = obj
        self.csv_files = csv_files

    def run(self):
        progressbar = self.obj.findChild(QProgressBar, "progressbar")
        det = MTCNNDetection(self.csv_files, './data/program_data', 32, (540, 648), device='cuda:0', same=False)
        face_files = det.detect_faces(num_workers=2, gui_params=(self.obj, self.pbar_sig))
        self.show_sig.emit(self.obj, QFrame, 'find-faces', 'hide')
        self.show_sig.emit(self.obj, QFrame, 'cluster-faces', 'show')
        self.finish.emit(self.obj, face_files)

class ClusteringThread(QtCore.QThread):

    pbar_sig = QtCore.pyqtSignal(QMainWindow, int, int)
    show_sig = QtCore.pyqtSignal(QMainWindow, type, str, str)
    finish = QtCore.pyqtSignal(QMainWindow, list)

    def __init__(self, obj, csv_files, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.obj = obj
        self.csv_files = csv_files

    def run(self):
        fe = FeatureExtractor(self.csv_files, './data/program_data', torch.device('cuda:0'), margin=10)
        features_files = fe.extract_features(pbar_emit_signal=lambda v: self.pbar_sig.emit(self.obj, 2, v))
        clusters = cluster_faces(features_files[0], None)
        save_images_with_bboxes(clusters, self.csv_files[0], './output', pbar_emit_signal=lambda v: self.pbar_sig.emit(self.obj, 4, v))
        self.show_sig.emit(self.obj, QFrame, 'cluster-faces', 'hide')
        self.finish.emit(self.obj, [1, 2])

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
