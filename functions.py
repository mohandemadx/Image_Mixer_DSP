from clickableLabel import QClickableLabel
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import image
from PyQt5.QtGui import QPixmap, QImage
import cv2
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtGui import QImage, QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QGraphicsSceneMouseEvent

def clear(frame):
    layout = frame.layout()
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

def create_images(image_num, frame):
    clear(frame)
    images_list = []

    layout = frame.layout()

    for i in range(image_num):
        image = QClickableLabel(f"lol{i}")
        images_list.append(image)
        
        layout.addWidget(image)

    frame.setLayout(layout)
    return images_list

def plot_fourier_component(real_part, imaginary_part, magnitude_spectrum, phase_spectrum ,label, index,width=0,heigth=0):
    try:
                if index == 0:
                    q_img =convert_component_to_qimage(real_part)
                    q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_img))
                    scene = QGraphicsScene()
                    scene.addItem(q_pixmap)
                    label.setScene(scene)
                    label.fitInView(q_pixmap, Qt.KeepAspectRatio)
                    addResizableRectangle(scene,q_img,width,heigth)
                    # label.setPixmap(q_img)
                    # label.setScaledContents(True)
                    # label.setWindowTitle('Real Part')
                elif index == 1:
                    q_img = convert_component_to_qimage(imaginary_part)
                    q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_img))
                    scene = QGraphicsScene()
                    scene.addItem(q_pixmap)
                    label.setScene(scene)
                    label.fitInView(q_pixmap, Qt.KeepAspectRatio)
                    addResizableRectangle(scene, q_img,width,heigth)
                    # label.setPixmap(q_img)
                    # label.setScaledContents(True)
                    # label.setWindowTitle('Imaginary Part')
                elif index == 2:
                    q_img = convert_component_to_qimage(phase_spectrum)
                    q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_img))
                    scene = QGraphicsScene()
                    scene.addItem(q_pixmap)
                    label.setScene(scene)
                    label.fitInView(q_pixmap, Qt.KeepAspectRatio)
                    addResizableRectangle(scene, q_img,width,heigth)
                    # label.setPixmap(q_img)
                    # label.setScaledContents(True)
                    # label.setWindowTitle('Phase Spectrum')

                else:
                    # Ensure magnitude_spectrum is not modified in-place
                    magnitude_spectrum = np.log1p(np.clip(magnitude_spectrum, 0, None).copy())

                    # Check for NaN values and replace with a default value
                    if np.isnan(np.sum(magnitude_spectrum)):
                        print("Warning: Invalid values encountered in magnitude_spectrum. Replacing with zeros.")
                        magnitude_spectrum = np.zeros_like(magnitude_spectrum)

                        # Convert NumPy array to QPixmap for display
                    q_img = convert_component_to_qimage(magnitude_spectrum)
                    q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_img))
                    scene = QGraphicsScene()
                    scene.addItem(q_pixmap)
                    label.setScene(scene)
                    label.fitInView(q_pixmap, Qt.KeepAspectRatio)
                    addResizableRectangle(scene, q_img,width,heigth)
                    # label.setPixmap(q_img)
                    # label.setScaledContents(True)
                    # label.setWindowTitle('Magnitude Spectrum')
    except Exception as e:
        print(f"Error in displaying image: {e}")
def convert_component_to_qimage(component):
    # Normalize the component values to the range [0, 255] and convert to uint8
    component = (component / np.max(component) * 255).astype(np.uint8)
    height, width= component.shape
    # Calculate the number of bytes per line in the image
    bytes_per_line = component.shape[1]

    # Create a QImage from the component data
    q_image = QImage(component.data.tobytes(), width, height, bytes_per_line, QImage.Format_Grayscale8)

    #     return q_pixmap

    # Return the QImage object
    return q_image
def addResizableRectangle(scene,image_component,width,heigth):
    rect_item = QGraphicsRectItem(0, 0, width, heigth)
    rect_item.setPen(QPen(Qt.yellow))  # Set pen color to yellow
    brush = QBrush(QColor(255, 255, 0, 50))
    rect_item.setBrush(brush)
    rect_item.setPos((image_component.width() - rect_item.rect().width()) / 2,(image_component.height() - rect_item.rect().height()) / 2)
    scene.addItem(rect_item)

