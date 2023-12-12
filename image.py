from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np

class Image:
    def __init__(self, image_path, width, height):
        self.image_path = image_path
        self.width = width
        self.height = height
        self.image = self.read_image

    def read_image(self):
        image = cv2.imread(self.image_path,0)
        if (image.shape[0] != self.width) & (image.shape[1] != self.height) :
            image = cv2.resize(image, (self.width,self.height))
            return image

    def set_image(self, image_path, image_label):
        # Load image and display it in the QLabel
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setFixedSize(pixmap.size())
        
    def calculate_img_magnitude_phase(self):
        # Perform Fourier transform
        f_transform = np.fft.fft2(self.image)
        f_transform_shifted = np.fft.fftshift(f_transform)

        # Compute real and imaginary parts
        self.real_part = np.real(f_transform_shifted)
        self.imaginary_part = np.imag(f_transform_shifted)

        # Compute magnitude and phase
        self.magnitude_spectrum = np.abs(f_transform_shifted)
        self.phase_spectrum = np.angle(f_transform_shifted)
        
        