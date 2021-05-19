import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QStatusBar, QToolBar, QFrame, QGridLayout, QVBoxLayout

def create_button(icon_path, text):
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
    wrapper.setStyleSheet(
        """
        * {
            max-width: 100px;
            margin: 0px;
            border: none;
            border-radius: 10px;
            background-color: white;
            height: 80px;
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



class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Clusterer')
        self.setFixedWidth(1500)
        self._createCentralWidget()


    def _createCentralWidget(self):
        main_frame = QFrame()
        grid = QGridLayout()
        main_frame.setLayout(grid)

        sidebar = QFrame()
        sidebar_grid = QVBoxLayout()
        sidebar.setLayout(sidebar_grid)
        sidebar.setStyleSheet(
            """
            margin: 10px;
            """
        )
        sidebar_grid.addWidget(create_button('./static/open-folder.png', 'Open Folder'), 1)
        sidebar_grid.addWidget(create_button('./static/find-faces.png', 'Find Faces'), 2)
        sidebar_grid.addWidget(create_button('./static/find-faces.png', 'Temp Button'), 2)
        sidebar_grid.addWidget(create_button('./static/find-faces.png', 'Testing'), 2)

        content = QFrame()
        content.setStyleSheet(
            """
            margin: 10px;
            background-color: cyan;
            border: 2px solid red;
            """
        )

        grid.addWidget(sidebar, 0, 0)
        grid.addWidget(content, 0, 1, 1, 10)


        self.setCentralWidget(main_frame)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
