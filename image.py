from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import cv2

class Image:
    def __init__(self, image_path, width, height):
        self.image_path = image_path
        self.width = width
        self.height = height
        self.read_image
        
    def read_image(self):
        self.image = cv2.imread(self.image_path,0)
        if (self.image.shape[0] != self.width) & (self.image.shape[1] != self.height) :
            self.image = cv2.resize(self.image, (self.width,self.height))

    def set_image(self, image_path, image_label):
        # Load image and display it in the QLabel
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setFixedSize(pixmap.size())
        
