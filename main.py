import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDesktopWidget
from PyQt5.QtGui import QPixmap, QImage
from os import path
from image import Image
import functions as f
import numpy as np
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtGui import QImage, QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QGraphicsSceneMouseEvent

from PyQt5.uic import loadUiType

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "untitled.ui"))


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.setWindowTitle("Image Mixer")

        # Variables
        self.filters = "Images (*.png *.jpg *.bmp)"
        self.components=[]
        self.all_images_components=[]
        self.images_list=[]

        # Signals
        self.image1.mouseDoubleClickEvent = lambda event: self.double_click_event_handler(event, self.image1,self.Gimage1)
        self.image2.mouseDoubleClickEvent = lambda event: self.double_click_event_handler(event, self.image2,self.Gimage2)
        self.image3.mouseDoubleClickEvent = lambda event: self.double_click_event_handler(event, self.image3,self.Gimage3)
        self.image4.mouseDoubleClickEvent = lambda event: self.double_click_event_handler(event, self.image4,self.Gimage4)

        self.image1.setMouseTracking(True)
        self.image1.mouseMoveEvent = lambda event: self.on_label_mouse_move(event, self.image1)

        self.image2.setMouseTracking(True)
        self.image2.mouseMoveEvent = lambda event: self.on_label_mouse_move(event, self.image2)

        self.image3.setMouseTracking(True)
        self.image3.mouseMoveEvent = lambda event: self.on_label_mouse_move(event, self.image3)

        self.image4.setMouseTracking(True)
        self.image4.mouseMoveEvent = lambda event: self.on_label_mouse_move(event, self.image4)

        self.Fourier_comboBox_1.currentIndexChanged.connect(lambda:f.plot_fourier_component(self.all_images_components[0][0], self.all_images_components[0][1],self.all_images_components[0][2] ,self.all_images_components[0][3],self.Gimage1,self.Fourier_comboBox_1.currentIndex(),self.region_selecter1.value(),self.region_selecter1.value()))
        self.Fourier_comboBox_2.currentIndexChanged.connect(
            lambda: f.plot_fourier_component(self.all_images_components[1][0], self.all_images_components[1][1],
                                             self.all_images_components[1][2], self.all_images_components[1][3],
                                             self.Gimage2, self.Fourier_comboBox_2.currentIndex(), self.region_selecter2.value(), self.region_selecter2.value()))
        self.Fourier_comboBox_3.currentIndexChanged.connect(
            lambda: f.plot_fourier_component(self.all_images_components[2][0], self.all_images_components[2][1],
                                             self.all_images_components[2][2], self.all_images_components[2][3],
                                             self.Gimage3, self.Fourier_comboBox_3.currentIndex(), self.region_selecter3.value(),self.region_selecter3.value()))
        self.Fourier_comboBox_4.currentIndexChanged.connect(
            lambda: f.plot_fourier_component(self.all_images_components[3][0], self.all_images_components[3][1],
                                             self.all_images_components[3][2], self.all_images_components[3][3],
                                             self.Gimage4, self.Fourier_comboBox_4.currentIndex(), self.region_selecter4.value(), self.region_selecter4.value()))

        self.region_selecter1.valueChanged.connect(lambda:f.plot_fourier_component(self.all_images_components[0][0], self.all_images_components[0][1],self.all_images_components[0][2] ,self.all_images_components[0][3],self.Gimage1,self.Fourier_comboBox_1.currentIndex(),self.region_selecter1.value(),self.region_selecter1.value()))
        self.region_selecter2.valueChanged.connect(
            lambda: f.plot_fourier_component(self.all_images_components[1][0], self.all_images_components[1][1],
                                             self.all_images_components[1][2], self.all_images_components[1][3],
                                             self.Gimage2, self.Fourier_comboBox_2.currentIndex(),
                                             self.region_selecter2.value(), self.region_selecter2.value()))
        self.region_selecter3.valueChanged.connect( lambda: f.plot_fourier_component(self.all_images_components[2][0], self.all_images_components[2][1],
                                             self.all_images_components[2][2], self.all_images_components[2][3],
                                             self.Gimage3, self.Fourier_comboBox_3.currentIndex(), self.region_selecter3.value(),self.region_selecter3.value()))
        self.region_selecter4.valueChanged.connect( lambda: f.plot_fourier_component(self.all_images_components[3][0], self.all_images_components[3][1],
                                             self.all_images_components[3][2], self.all_images_components[3][3],
                                             self.Gimage4, self.Fourier_comboBox_4.currentIndex(), self.region_selecter4.value(), self.region_selecter4.value()))
    # Functions
    def double_click_event_handler(self, event, label,fourier_label):
        try:
            if event.button() == Qt.LeftButton:
                # Call the upload function when label is double-clicked
                self.upload(label, fourier_label)
        except Exception as e:
            print(f"Error in double_click_event_handler: {e}")

    def upload(self, label,fourier_label):
        filters = "Images (*.jpg *.jpeg *.png);;All Files (*)"
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileNames()", "", filters,
                                                   options=options)

        if file_path:

            # Load images asynchronously
            image = Image(file_path, width=218, height=116)  # Set width and height accordingly
            image.set_image(label)
            self.current_image_path=file_path
            self.images_list.append(image)

            # Perform Fourier transform asynchronously
            self.load_fourier_component(image,fourier_label)

    def load_fourier_component(self, image,fourier_label):
        try:
            image_for_fourier = image.read_image()
            self.real_part, self.imaginary_part, self.magnitude_spectrum, self.phase_spectrum = image.calculate_img_magnitude_phase(
                image_for_fourier)
            components=[self.real_part,self.imaginary_part,self.magnitude_spectrum,self.phase_spectrum]

            if fourier_label == self.Gimage1:
                self.all_images_components.insert(0, components)
            elif fourier_label == self.Gimage2:
                self.all_images_components.insert(1, components)
            elif fourier_label == self.Gimage3:
                self.all_images_components.insert(2, components)
            elif fourier_label == self.Gimage4:
                self.all_images_components.insert(3, components)
            else:
                print(f"Unsupported Fourier label: {fourier_label}")
            f.plot_fourier_component(self.magnitude_spectrum, self.real_part, self.imaginary_part,self.phase_spectrum,fourier_label,self.Fourier_comboBox_1.currentIndex())
        except Exception as e:
            print(f"Error loading Fourier component: {e}")

    def on_label_mouse_move(self, event, label):
        try:
            if event.buttons() & Qt.LeftButton:
                # Adjust brightness based on mouse position
                width = label.width()
                mouse_x = event.x()

                # Normalize mouse position to brightness factor
                normalized_factor = mouse_x / width
                factor_range = 2.0  # Adjust the range as needed
                brightness_factor = normalized_factor * factor_range
                if label== self.image1:
                    image=self.images_list[0]
                    image.adjust_brightness(brightness_factor, label)
                if label == self.image2:
                    image = self.images_list[1]
                    image.adjust_brightness(brightness_factor, label)
                if label == self.image3:
                    image = self.images_list[2]
                    image.adjust_brightness(brightness_factor, label)
                if label == self.image4:
                        image = self.images_list[3]
                        image.adjust_brightness(brightness_factor, label)

        except Exception as e:
            print(f"Error in on_label_mouse_move: {e}")
    def closeEvent(self, event):
        # Release resources when the window is closed
        cv2.destroyAllWindows()


def main():
    app = QApplication(sys.argv)

    # with open("style.qss", "r") as f:
    #     _style = f.read()
    #     app.setStyleSheet(_style)

    window = MainApp()

    # Center the window on the screen
    screen_geometry = app.desktop().availableGeometry()
    window_geometry = window.frameGeometry()
    window.move((screen_geometry.width() - window_geometry.width()) // 2,
                (screen_geometry.height() - window_geometry.height()) // 2)

    # Show the window without maximizing
    window.showNormal()

    app.exec_()


if __name__ == '__main__':
    main()
