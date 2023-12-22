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
        self.sliders_list=[self.weight_1,self.weight_2,self.weight_3,self.weight_4]
        self.combobox_list=[self.Fourier_comboBox_1,self.Fourier_comboBox_2,self.Fourier_comboBox_3,self.Fourier_comboBox_4]
        self.components_weights={0:0,1:0,2:0,3:0} #index of combobox and corresponding slider value
        self.image_dict = {
            self.image1: None,
            self.image2: None,
            self.image3: None,
            self.image4: None
        }

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

        self.Fourier_comboBox_1.currentIndexChanged.connect(lambda:f.plot_fourier_component(self.image_dict[self.image1].components[0],self.image_dict[self.image1].components[1] ,self.image_dict[self.image1].components[2],self.image_dict[self.image1].components[3],self.Gimage1,self.Fourier_comboBox_1.currentIndex(),self.region_selecter.value(),self.region_selecter.value()))
        self.Fourier_comboBox_2.currentIndexChanged.connect(lambda:f.plot_fourier_component(self.image_dict[self.image2].components[0],self.image_dict[self.image2].components[1] ,self.image_dict[self.image2].components[2],self.image_dict[self.image2].components[3],self.Gimage2,self.Fourier_comboBox_2.currentIndex(),self.region_selecter.value(),self.region_selecter.value()))
        self.Fourier_comboBox_3.currentIndexChanged.connect(lambda:f.plot_fourier_component(self.image_dict[self.image3].components[0],self.image_dict[self.image3].components[1] ,self.image_dict[self.image3].components[2],self.image_dict[self.image3].components[3],self.Gimage3,self.Fourier_comboBox_3.currentIndex(),self.region_selecter.value(),self.region_selecter.value()))
        self.Fourier_comboBox_4.currentIndexChanged.connect(lambda:f.plot_fourier_component(self.image_dict[self.image4].components[0],self.image_dict[self.image4].components[1] ,self.image_dict[self.image4].components[2],self.image_dict[self.image4].components[3],self.Gimage4,self.Fourier_comboBox_4.currentIndex(),self.region_selecter.value(),self.region_selecter.value()))

        self.region_selecter.valueChanged.connect(self.apply_region)
        self.apply_mixer.clicked.connect(self.mixer)
        # self.real_imaginary.toggled.connect(self.components_selection)

    # Functions
    def apply_region(self,value):
            try:
                f.plot_fourier_component(self.image_dict[self.image1].components[0],self.image_dict[self.image1].components[1] ,self.image_dict[self.image1].components[2],self.image_dict[self.image1].components[3],self.Gimage1,self.Fourier_comboBox_1.currentIndex(),value,value)
            except Exception as e:
                print(f"Error in apply_region (index 0): {e}")

            try:
                f.plot_fourier_component(
                    self.image_dict[self.image2].components[0],
                    self.image_dict[self.image2].components[1],
                    self.image_dict[self.image2].components[2],
                    self.image_dict[self.image2].components[3],
                    self.Gimage2,
                    self.Fourier_comboBox_2.currentIndex(),
                    value,
                    value
                )
            except Exception as e:
                print(f"Error in apply_region (index 1): {e}")

            try:
                f.plot_fourier_component(
                    self.image_dict[self.image3].components[0],
                    self.image_dict[self.image3].components[1],
                    self.image_dict[self.image3].components[2],
                    self.image_dict[self.image3].components[3],
                    self.Gimage3,
                    self.Fourier_comboBox_3.currentIndex(),
                    value,
                    value
                )
            except Exception as e:
                print(f"Error in apply_region (index 2): {e}")

            try:
                f.plot_fourier_component(
                    self.image_dict[self.image4].components[0],
                    self.image_dict[self.image4].components[1],
                    self.image_dict[self.image4].components[2],
                    self.image_dict[self.image4].components[3],
                    self.Gimage4,
                    self.Fourier_comboBox_4.currentIndex(),
                    value,
                    value
                )
            except Exception as e:
                print(f"Error in apply_region (index 3): {e}")

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
            image = Image(file_path, width=218, height=116)
            image.set_image(label)
            self.current_image_path=file_path
            self.image_dict[label]=image
            #self.images_list.append(image)

            # Perform Fourier transform asynchronously
            self.load_fourier_component(image,fourier_label)



    def load_fourier_component(self, image,fourier_label):
        try:
            components=image.components
            f.plot_fourier_component(components[0], components[2], components[1],components[3],fourier_label,self.Fourier_comboBox_1.currentIndex())
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
                image = self.image_dict[label]
                image.adjust_brightness(brightness_factor, label)

        except Exception as e:
            print(f"Error in on_label_mouse_move: {e}")


    def closeEvent(self, event):
        # Release resources when the window is closed
        cv2.destroyAllWindows()

    # def mixer(self):
    #         weights = [slider.value()/100 for slider in self.sliders_list]
    #         chosen_comp=[combobox.currentIndex() for combobox in self.combobox_list]
    #
    #         for i,label in enumerate[self.image1,self.image2,self.image3,self.image4]:
    #             weighted_sum += self.image_dict[label].components[chosen_comp[i]]*weights[i]


    def mixer(self):
        try:
            image_keys = [self.image1, self.image2, self.image3, self.image4]

            real_array = [self.image_dict[key].components[0] for key in image_keys]
            imaginary_array = [self.image_dict[key].components[1] for key in image_keys]
            phase_array = [self.image_dict[key].components[3] for key in image_keys]
            magnitudes_array = [self.image_dict[key].components[2] for key in image_keys]

            # Find the maximum shape among the arrays
            max_shape = max(arr.shape for arr in real_array + imaginary_array + phase_array + magnitudes_array)
            imaginary_sum = np.zeros(max_shape, dtype=np.float32)
            real_sum = np.zeros(max_shape, dtype=np.float32)
            mag_sum = np.zeros(max_shape, dtype=np.float32)
            phase_sum = np.zeros(max_shape, dtype=np.float32)

            # Resize each array to the maximum shape
            resized_real_array = [cv2.resize(arr, max_shape[::-1]) for arr in real_array]
            resized_imaginary_array = [cv2.resize(arr, max_shape[::-1]) for arr in imaginary_array]
            resized_phase_array = [cv2.resize(arr, max_shape[::-1]) for arr in phase_array]
            resized_magnitudes_array = [cv2.resize(arr, max_shape[::-1]) for arr in magnitudes_array]

            mag_weights = [
                slider.value()/100 * np.ones(max_shape, dtype=np.float32) if combobox.currentIndex() == 2 else np.zeros(
                    max_shape, dtype=np.float32) for slider, combobox in zip(self.sliders_list, self.combobox_list)]
            phase_weights = [
                slider.value()/100 * np.ones(max_shape, dtype=np.float32) if combobox.currentIndex() == 3 else np.zeros(
                    max_shape, dtype=np.float32) for slider, combobox in zip(self.sliders_list, self.combobox_list)]
            imaginary_weights = [
                slider.value()/100 * np.ones(max_shape, dtype=np.float32) if combobox.currentIndex() == 1 else np.zeros(
                    max_shape, dtype=np.float32) for slider, combobox in zip(self.sliders_list, self.combobox_list)]
            real_weights = [
                slider.value()/100 * np.ones(max_shape, dtype=np.float32) if combobox.currentIndex() == 0 else np.zeros(
                    max_shape, dtype=np.float32) for slider, combobox in zip(self.sliders_list, self.combobox_list)]
            # mag_weights = [slider.value() if combobox.currentIndex() == 2 else 0 for slider, combobox in
            #                zip(self.sliders_list, self.combobox_list)]
            # phase_weights = [slider.value() if combobox.currentIndex() == 3 else 0 for slider, combobox in
            #                  zip(self.sliders_list, self.combobox_list)]
            # imaginary_weights = [slider.value() if combobox.currentIndex() == 1 else 0 for slider, combobox in
            #                      zip(self.sliders_list, self.combobox_list)]
            # real_weights = [slider.value() if combobox.currentIndex() == 0 else 0 for slider, combobox in
            #                 zip(self.sliders_list, self.combobox_list)]

            # print("Shapes of arrays:")
            # for i, mag_arr in enumerate(magnitudes_array):
            #     print(f"magnitudes_array[{i}]:", np.shape(mag_arr))
            #
            # print("phase_array:", np.shape(phase_array))
            # print("imaginary_array:", np.shape(imaginary_array))
            # print("real_array:", np.shape(real_array))
            if self.real_imaginary.isChecked():
                for i in range(4):
                    imaginary_sum += resized_imaginary_array[i] * imaginary_weights[i]
                    real_sum += resized_real_array[i] * real_weights[i]
                mixed_image = np.fft.ifft2(np.fft.ifftshift(real_sum + 1j * imaginary_sum))
                final_mixed_image=np.abs(mixed_image).astype(np.uint8)
                f.display_output_image(self.output_mixer1, final_mixed_image)

            elif self.magnitude_phase.isChecked():
                for i in range(4):
                    mag_sum += resized_magnitudes_array[i] * mag_weights[i]
                    phase_sum += resized_phase_array[i] * phase_weights[i]
                mixed_image = np.fft.ifft2(np.fft.ifftshift(mag_sum * np.exp(1j * phase_sum)))
                final_mixed_image = np.abs(mixed_image).astype(np.uint8)
                f.display_output_image(self.output_mixer1, final_mixed_image)

            else:
                print("Error: No mixing option selected.")

        except Exception as e:
            print(f"Error during image mixing: {e}")


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
