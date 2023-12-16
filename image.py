from PyQt5.QtGui import QPixmap, QImage
import cv2
from matplotlib import pylab
import numpy as np
import matplotlib as plt
from PIL import Image as PILImage

class Image:

    def __init__(self, image_path, width, height):
        self.image_path = image_path
        self.width = width
        self.height = height
        self.image = self.read_image



    def read_image(self):
        try:
            image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

            # Optionally, resize the image based on width and height parameters
            if self.width > 0 and self.height > 0:
                image = cv2.resize(image, (self.width, self.height))

            return image
        except Exception as e:
            print(f"Error in read_image: {e}")
            return None


    def set_image(self, image_label):
        image = self.read_image()

        if image is not None:
            try:
                q_image = self.convert_image_to_qimage(image)
                q_image_resized = q_image.scaled(image_label.size())
                image_label.setPixmap(QPixmap.fromImage(q_image_resized))
                image_label.setFixedSize(image_label.size())
            except Exception as e:
                print(f"Error in set_image: {e}")


    def convert_image_to_qimage(self, image):
            try:
                height, width = image.shape[:2]
                bytes_per_line = 1 * width
                q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

                return q_image
            except Exception as e:
                print(f"Error in convert_image_to_qimage: {e}")
                return None


    def calculate_img_magnitude_phase(self, image):
            try:
                f_transform = np.fft.fft2(image)
                f_transform_shifted = np.fft.fftshift(f_transform)
                real_part = np.real(f_transform_shifted)
                imaginary_part = np.imag(f_transform_shifted)
                magnitude_spectrum = np.abs(f_transform_shifted)
                phase_spectrum = np.angle(f_transform_shifted)

                return real_part, imaginary_part, magnitude_spectrum, phase_spectrum
            except Exception as e:
                print(f"Error in calculate_img_magnitude_phase: {e}")
                return None, None, None, None