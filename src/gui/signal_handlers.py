import threading
from PyQt5.QtWidgets import QProgressBar

def update_progressbar(obj, value):
    checkbox = obj.findChild(QProgressBar, "progressbar")
    checkbox.setValue(value)

def op_widget(obj, type, name, op):
    widget = obj.findChild(type, name)
    if op == 'hide':
        widget.hide()
    elif op == 'show':
        widget.show()
    elif op == 'clear':
        widget.clear()
