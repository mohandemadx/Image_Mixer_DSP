from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class QClickableLabel(QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Label Clicked!")

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Label Double-Clicked!")