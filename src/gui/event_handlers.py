import os
import cv2
import sys
import shutil
from PyQt5 import QtCore
import matplotlib.pyplot as plt
from PyQt5.QtGui import QCursor, QMovie, QPixmap, QImage, QBrush, QPainter, QWindow
from PyQt5.QtWidgets import QFileDialog, QFrame, QPushButton, QLineEdit, QProgressBar, QLabel
from src.gui.worker_threads import TempProgressBarThread, ImageDiscoveryThread, FaceDetectionThread

# ------------------------------------------ EVENT HANDLERS ------------------------------------------
def open_folder(obj, loading_section):
    folder = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
    if folder == '':
        return
    add_animation(loading_section)
    obj.t1 = ImageDiscoveryThread(obj, folder)
    obj.t1.sig.connect(op_widget)
    obj.t1.finish.connect(image_discovery_finsihed)
    obj.t1.daemon = True
    obj.t1.start()

def close_folder(obj):
    open_folder_button = obj.findChild(QFrame, 'open-folder')
    close_folder_button = obj.findChild(QFrame, 'close-folder')
    find_faces = obj.findChild(QFrame, 'find-faces')
    pbar = obj.findChild(QProgressBar, 'progressbar')
    close_folder_button.hide()
    open_folder_button.show()
    find_faces.hide()
    pbar.hide()
    tab_frame1 = obj.findChild(QFrame, 'tab-frame1')
    clear_layout(tab_frame1.layout())
    obj.program_state.deactivate_tab(1)
    obj.program_state.deactivate_tab(2)
    obj.program_state.deactivate_tab(3)
    switch_tab(obj, 1)
    setup_empty_folder()

def detect_faces(obj):
    csv_files = obj.imported_images
    pbar = obj.findChild(QProgressBar, 'progressbar')
    pbar.show()
    obj.t2 = FaceDetectionThread(obj, csv_files)
    obj.t2.sig.connect(update_progressbar)
    obj.t2.finish.connect(detection_finished)
    obj.t2.daemon = True
    obj.t2.start()

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

    obj.program_state.change_tab(tab_number)
    reload_page_number(obj)
    reload_total_pages(obj)

def go_next(obj):
    change_page(obj, obj.program_state.whereami()[1] + 1)

def go_back(obj):
    change_page(obj, obj.program_state.whereami()[1] - 1)

def change_page(obj, page_number):
    current_tab, _ = obj.program_state.whereami()
    if current_tab == 1:
        if page_number > obj.pg1.total_pages() or page_number < 1:
            print('Page out of bound')
            return
        obj.program_state.change_page(page_number)
        reload_page_number(obj)
        items = obj.pg1.page(page_number)
        tab_frame1 = obj.findChild(QFrame, 'tab-frame1')
        tab_frame1_layout = tab_frame1.layout()
        clear_layout(tab_frame1_layout)
        for i, row in items.iterrows():
            img = QPixmap(row['path'])
            img = img.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
            y = QLabel()
            y.setAlignment(QtCore.Qt.AlignCenter)
            y.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            y.setPixmap(img)
            # y.installEventFilter()
            # y.mousePressEvent = image_clicked
            tab_frame1_layout.addWidget(y, i / 5, i % 5)

    elif obj.program_state.whereami()[0] == 2:
        if page_number > obj.pg2.total_pages() or page_number < 1:
            print('Page out of bound')
            return
        obj.program_state.change_page(page_number)
        reload_page_number(obj)
        items = obj.pg2.page(page_number)
        tab_frame2 = obj.findChild(QFrame, 'tab-frame2')
        tab_frame2_layout = tab_frame2.layout()
        clear_layout(tab_frame2_layout)
        for i, row in items.iterrows():
            img = create_pixmap_image(row['image_path'], [row['x_from_per'], row['y_from_per'], row['x_to_per'], row['y_to_per']], size=(200, 200))
            y = QLabel()
            y.setAlignment(QtCore.Qt.AlignCenter)
            y.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            y.setPixmap(img)
            # y.installEventFilter()
            # y.mousePressEvent = image_clicked
            tab_frame2_layout.addWidget(y, i / 5, i % 5)

# def image_clicked(event):
#     print(event.button())

# def select_image(obj, name):
#     obj.selected_images.append(name)

# def unselect_image(obj, name):
#     pass

# ------------------------------------------ SLOTS ------------------------------------------
def update_progressbar(obj, value):
    checkbox = obj.findChild(QProgressBar, "progressbar")
    checkbox.setValue(max(13, value))

def op_widget(obj, type, name, op):
    widget = obj.findChild(type, name)
    if op == 'hide':
        widget.hide()
    elif op == 'show':
        widget.show()
    elif op == 'clear':
        widget.clear()

def image_discovery_finsihed(obj, files):
    obj.create_first_paginator(files)
    obj.imported_images = files
    obj.program_state.activate_tab(1)
    switch_tab(obj, 1)
    change_page(obj, 1)

def detection_finished(obj, files):
    obj.create_second_paginator(files)
    obj.detected_faces = files
    obj.program_state.activate_tab(2)
    switch_tab(obj, 2)
    change_page(obj, 1)

# ------------------------------------------ UTILS ------------------------------------------
def add_animation(wrapper):
    ani = QMovie('./static/loading-gif.gif')
    ani.setScaledSize(QtCore.QSize(80, 80))
    wrapper.setMovie(ani)
    ani.start()
    return wrapper

def reload_page_number(obj):
    page_input = obj.findChild(QLineEdit, 'page-input')
    page_input.setText('{}'.format(obj.program_state.whereami()[1]))

def reload_total_pages(obj):
    page_label = obj.findChild(QLabel, 'page-label')
    page_label.setText('/{}'.format(obj.get_current_paginator().total_pages()))

def clear_layout(layout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        if not item:
            continue
        w = item.widget()
        if w:
            w.deleteLater()

def setup_empty_folder(path='./program_data'):
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


def create_pixmap_image(image_path, bbox, size=(100, 100), imgtype='png'):
    img = cv2.imread(image_path)[:, :, ::-1]
    x_from = max(int(bbox[0] * img.shape[1] / 100), 0)
    y_from = max(int(bbox[1] * img.shape[0] / 100), 0)
    x_to = min(int(bbox[2] * img.shape[1] / 100), img.shape[1])
    y_to = min(int(bbox[3] * img.shape[0] / 100), img.shape[0])
    img = img[y_from:y_to, x_from:x_to, :]
    pix = QImage(img.data.tobytes(), img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
    return QPixmap(pix).scaled(size[0], size[1])
