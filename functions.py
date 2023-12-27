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

def plot_fourier_component(real_part, imaginary_part, magnitude_spectrum, phase_spectrum ,label, index,width=0,heigth=0):
    try:
                if index == 0:
                    q_img =convert_component_to_qimage(real_part)
                    q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_img))
                    scene = QGraphicsScene()
                    scene.addItem(q_pixmap)
                    label.setScene(scene)
                    label.fitInView(q_pixmap, Qt.KeepAspectRatio)
                    return scene,q_img,real_part
                    # addResizableRectangle(scene,q_img,real_part,width,heigth)

                elif index == 1:
                    q_img = convert_component_to_qimage(imaginary_part)
                    q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_img))
                    scene = QGraphicsScene()
                    scene.addItem(q_pixmap)
                    label.setScene(scene)
                    label.fitInView(q_pixmap, Qt.KeepAspectRatio)
                    return scene,q_img,imaginary_part
                    # addResizableRectangle(scene, q_img,imaginary_part,width,heigth)

                elif index == 3:
                    q_img = convert_component_to_qimage(phase_spectrum)
                    q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_img))
                    scene = QGraphicsScene()
                    scene.addItem(q_pixmap)
                    label.setScene(scene)
                    label.fitInView(q_pixmap, Qt.KeepAspectRatio)
                    return scene,q_img,phase_spectrum
                    # addResizableRectangle(scene, q_img,phase_spectrum,width,heigth)


                elif index==2:
                    # Ensure magnitude_spectrum is not modified in-place
                    magnitude_spectrum_plotted = np.multiply(np.log10(1 + magnitude_spectrum), 20)

                        # Convert NumPy array to QPixmap for display
                    q_img = convert_component_to_qimage(magnitude_spectrum_plotted)
                    q_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(q_img))
                    scene = QGraphicsScene()
                    scene.addItem(q_pixmap)
                    label.setScene(scene)
                    label.fitInView(q_pixmap, Qt.KeepAspectRatio)
                    return scene,q_img,magnitude_spectrum
                    # addResizableRectangle(scene, q_img,magnitude_spectrum,width,heigth)

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



def addResizableRectangle(scene,image_component,width,height,inner_rect):
    rect_item = QGraphicsRectItem(0, 0, width, height)
    rect_center_x = (image_component.width() - rect_item.rect().width()) / 2
    rect_center_y = (image_component.height() - rect_item.rect().height()) / 2
    rect_item = QGraphicsRectItem(0, 0, width, height)
    rect_item.setPen(QPen(Qt.yellow))  # Set pen color to yellow
    brush = QBrush(QColor(255, 255, 0, 50))
    rect_item.setBrush(brush)
    rect_item.setPos(rect_center_x, rect_center_y)
    scene.addItem(rect_item)
    if not inner_rect.isChecked():
        brush = QBrush(QColor(0, 0, 0, 50))
        rect_item.setBrush(brush)
        rect_item.setPos(rect_center_x, rect_center_y)
        scene.addItem(rect_item)
        overlay_path = QPainterPath()
        overlay_path.addRect(0, 0, image_component.width(), image_component.height())
        rect_path = QPainterPath()
        rect_path.addRect(rect_center_x, rect_center_y, width, height)
        # Subtract rect_path from overlay_path
        overlay_path -= rect_path
        # Create a QGraphicsPathItem for the resulting path (difference)
        difference_item = scene.addPath(overlay_path, QPen(Qt.NoPen), QBrush(QColor(255, 255, 0, 50)))
    return rect_item






def ExtractRegion(rect_item, image_component, image_component_array, inner_region_selected):
    image_component = QGraphicsPixmapItem(QPixmap.fromImage(image_component))
    rect_scene_pos = rect_item.scenePos()
    rect_scene_rect = rect_item.rect()
    rect_image_pos = image_component.mapFromScene(rect_scene_pos)
    rect_image_rect = image_component.mapFromScene(rect_scene_rect).boundingRect()
    if inner_region_selected.isChecked():

        mask = np.zeros_like(image_component_array)
        mask[int(rect_image_pos.y()):int(rect_image_pos.y() + rect_image_rect.height()),
             int(rect_image_pos.x()):int(rect_image_pos.x() + rect_image_rect.width())] = 1
    else:

        mask = np.ones_like(image_component_array)
        mask[int(rect_image_pos.y()):int(rect_image_pos.y() + rect_image_rect.height()),
        int(rect_image_pos.x()):int(rect_image_pos.x() + rect_image_rect.width())] = 0
    image_component_array = image_component_array * mask
    return image_component_array


def display_output_image(label,mixed_image):
    # Convert NumPy array to QImage
    height, width = mixed_image.shape
    bytes_per_line = width
    q_image = QImage(mixed_image.data.tobytes(), width, height, bytes_per_line, QImage.Format_Grayscale8)

    # Display the mixed image in the QGraphicsView
    scene = QGraphicsScene()
    pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(q_image))
    scene.addItem(pixmap_item)

    label.setScene(scene)
    label.fitInView(pixmap_item, Qt.KeepAspectRatio)


