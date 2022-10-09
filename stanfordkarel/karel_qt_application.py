from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPalette, QColor


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Karel")
        # button = QPushButton("Press Me!")
        self.setFixedSize(QSize(800, 600))
        # Set the central widget of the Window.
        # self.setCentralWidget(button)

        layout = QHBoxLayout()

        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('black'))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(50, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)
