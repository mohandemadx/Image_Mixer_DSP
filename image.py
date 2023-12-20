from PyQt5.QtGui import QPixmap, QImage
import cv2
from matplotlib import pylab
import numpy as np
import matplotlib as plt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtGui import QImage, QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QGraphicsSceneMouseEvent

class Image:

    def __init__(self, image_path, width, height):
        self.image_path = image_path
        self.width = width
        self.height = height
        self.image = self.read_image



    def read_image(self):
        try:
            image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)


            return image
        except Exception as e:
            print(f"Error in read_image: {e}")
            return None


    def set_image(self, label):
        image = self.read_image()

        if image is not None:
            try:
                q_image = self.convert_image_to_qimage(image)
                q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_image))
                scene = QGraphicsScene()
                scene.addItem(q_pixmap)
                label.setScene(scene)
                label.fitInView(q_pixmap, Qt.KeepAspectRatio)
                # q_image_resized = q_image.scaled(image_label.size())
                # image_label.setPixmap(QPixmap.fromImage(q_image_resized))
                # image_label.setFixedSize(image_label.size())
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

    def adjust_brightness(self, factor, label):
        image = self.read_image()
        try:
                adjusted_image = self.adjust_brightness_opencv(image, factor)

                if adjusted_image is not None:
                    # Convert the adjusted image to QImage using OpenCV
                    q_image = self.convert_image_to_qimage(adjusted_image)

                    # Display the adjusted image in the label
                    q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_image))
                    scene = QGraphicsScene()
                    scene.addItem(q_pixmap)
                    label.setScene(scene)
                    label.fitInView(q_pixmap, Qt.KeepAspectRatio)

        except Exception as e:
                print(f"Error adjusting brightness: {e}")

    def adjust_brightness_opencv(self, image, factor):
        try:
            # Convert the image to float
            image_float = image.astype('float32') / 255.0

            # Adjust the brightness using OpenCV
            adjusted_image = cv2.multiply(image_float, factor)

            # Clip the values to stay within the valid range [0, 1]
            adjusted_image = np.clip(adjusted_image, 0, 1)

            # Convert back to uint8 format
            adjusted_image = (adjusted_image * 255).astype('uint8')

            return adjusted_image

        except Exception as e:
            print(f"Error in adjust_brightness_opencv: {e}")
            return None
