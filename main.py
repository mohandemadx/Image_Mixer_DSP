import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDesktopWidget, QButtonGroup
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
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QGraphicsSceneMouseEvent

from PyQt5.uic import loadUiType

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "untitled.ui"))


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)

        self.timer = None
        self.setupUi(self)
        self.setWindowTitle("Image Mixer")

        # Variables
        self.filters = "Images (*.png *.jpg *.bmp)"
        self.components =[]
        self.sliders_list=[self.weight_1,self.weight_2,self.weight_3,self.weight_4]
        self.combobox_list=[self.Fourier_comboBox_1,self.Fourier_comboBox_2,self.Fourier_comboBox_3,self.Fourier_comboBox_4]
        self.image_dict = {
            self.image1: None,
            self.image2: None,
            self.image3: None,
            self.image4: None
        }
        # Intial Settings
        self.Fourier_comboBox_1.model().item(2).setEnabled(False)
        self.Fourier_comboBox_2.model().item(2).setEnabled(False)
        self.Fourier_comboBox_3.model().item(2).setEnabled(False)
        self.Fourier_comboBox_4.model().item(2).setEnabled(False)
        self.Fourier_comboBox_1.model().item(3).setEnabled(False)
        self.Fourier_comboBox_2.model().item(3).setEnabled(False)
        self.Fourier_comboBox_3.model().item(3).setEnabled(False)
        self.Fourier_comboBox_4.model().item(3).setEnabled(False)
        self.region_selecter.setRange(0, 100)
        self.real_imaginary.isChecked()


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
        self.Fourier_comboBox_1.currentIndexChanged.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.Fourier_comboBox_2.currentIndexChanged.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.Fourier_comboBox_3.currentIndexChanged.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.Fourier_comboBox_4.currentIndexChanged.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.region_selecter.valueChanged.connect(self.apply_region)
        self.in_region_radioButton.toggled.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.out_region_radioButton.toggled.connect(lambda:self.apply_region(self.region_selecter.value()))
        self.real_imaginary.clicked.connect(self.update_combo_box)
        self.magnitude_phase.clicked.connect(self.update_combo_box)



        #Handling mixer instantenous changes
        for slider in self.sliders_list:
                slider.valueChanged.connect(self.mixer)
        for combobox in self.combobox_list:
            combobox.currentIndexChanged.connect(self.mixer)
        self.region_selecter.valueChanged.connect(self.mixer)
        self.in_region_radioButton.toggled.connect(self.mixer)
        self.out_region_radioButton.toggled.connect(self.mixer)
        self.real_imaginary.clicked.connect(self.mixer)
        self.magnitude_phase.clicked.connect(self.mixer)
        self.output1.toggled.connect(self.mixer)
        self.output2.toggled.connect(self.mixer)






    #Functions

    def apply_region(self,value):
            try:
                scene,q_img,img_comp=f.plot_fourier_component(self.image_dict[self.image1].components[0],self.image_dict[self.image1].components[1] ,self.image_dict[self.image1].components[2],self.image_dict[self.image1].components[3],self.Gimage1,self.Fourier_comboBox_1.currentIndex(),value,value)
                if self.out_region_radioButton.isChecked() or self.in_region_radioButton.isChecked():
                    rect_item=f.addResizableRectangle(scene,q_img,value,value,self.in_region_radioButton)
                    self.masked_img_comp1=f.ExtractRegion(rect_item,q_img,img_comp,self.in_region_radioButton)


            except Exception as e:
                print(f"Error in apply_region (index 0): {e}")

            try:
                scene2,q_img2,img_comp2=f.plot_fourier_component(
                    self.image_dict[self.image2].components[0],
                    self.image_dict[self.image2].components[1],
                    self.image_dict[self.image2].components[2],
                    self.image_dict[self.image2].components[3],
                    self.Gimage2,
                    self.Fourier_comboBox_2.currentIndex(),
                    value,
                    value
                )
                if self.out_region_radioButton.isChecked() or self.in_region_radioButton.isChecked():
                    rect_item2 = f.addResizableRectangle(scene2, q_img2, value, value, self.in_region_radioButton)
                    self.masked_img_comp2 = f.ExtractRegion(rect_item2, q_img2, img_comp2, self.in_region_radioButton)

            except Exception as e:
                print(f"Error in apply_region (index 1): {e}")

            try:
                scene3, q_img3, img_comp3=f.plot_fourier_component(
                    self.image_dict[self.image3].components[0],
                    self.image_dict[self.image3].components[1],
                    self.image_dict[self.image3].components[2],
                    self.image_dict[self.image3].components[3],
                    self.Gimage3,
                    self.Fourier_comboBox_3.currentIndex(),
                    value,
                    value
                )
                if self.out_region_radioButton.isChecked() or self.in_region_radioButton.isChecked():
                    rect_item3 = f.addResizableRectangle(scene3, q_img3, value, value, self.in_region_radioButton)
                    self.masked_img_comp3 = f.ExtractRegion(rect_item3, q_img3, img_comp3, self.in_region_radioButton)
            except Exception as e:
                print(f"Error in apply_region (index 2): {e}")

            try:
                scene4, q_img4, img_comp4=f.plot_fourier_component(
                    self.image_dict[self.image4].components[0],
                    self.image_dict[self.image4].components[1],
                    self.image_dict[self.image4].components[2],
                    self.image_dict[self.image4].components[3],
                    self.Gimage4,
                    self.Fourier_comboBox_4.currentIndex(),
                    value,
                    value
                )
                if self.out_region_radioButton.isChecked() or self.in_region_radioButton.isChecked():
                    rect_item4 = f.addResizableRectangle(scene4, q_img4, value, value, self.in_region_radioButton)
                    self.masked_img_comp4 = f.ExtractRegion(rect_item4, q_img4, img_comp4, self.in_region_radioButton)

            except Exception as e:
                print(f"Error in apply_region (index 3): {e}")
            self.masked_imgs = [self.masked_img_comp1, self.masked_img_comp2, self.masked_img_comp3,
                                self.masked_img_comp4]

    def double_click_event_handler(self, event, label,fourier_label):
        try:
            if event.button() == Qt.LeftButton:
                # Call the upload function when label is double-clicked
                self.upload(label, fourier_label)
        except Exception as e:
            print(f"Error in double_click_event_handler: {e}")
        try:
            if event.button() == Qt.RightButton:
                # Reset brightness to the original value
                for label in [self.image1, self.image2, self.image3, self.image4]:
                    image = self.image_dict[label]
                    if image:
                        image.adjust_brightness(1.0, label)  # Reset to original brightness

        except Exception as e:
            print(f"Error in mousePressEvent: {e}")

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



    def mixer(self):
        try:

            image_keys = [self.image1, self.image2, self.image3, self.image4]

            real_array = [self.image_dict[key].components[0] for key in image_keys]
            imaginary_array = [self.image_dict[key].components[1] for key in image_keys]
            phase_array = [self.image_dict[key].components[3] for key in image_keys]
            magnitudes_array = [self.image_dict[key].components[2] for key in image_keys]
            all_components=[real_array,imaginary_array,magnitudes_array,phase_array]
            self.apply_region(self.region_selecter.value())


            if self.in_region_radioButton.isChecked() or self.out_region_radioButton.isChecked():
                    all_components[self.Fourier_comboBox_1.currentIndex()][0]=self.masked_imgs[0]
                    all_components[self.Fourier_comboBox_2.currentIndex()][1] = self.masked_imgs[1]
                    all_components[self.Fourier_comboBox_3.currentIndex()][2] = self.masked_imgs[2]
                    all_components[self.Fourier_comboBox_4.currentIndex()][3] = self.masked_imgs[3]


            # Find the maximum shape among the arrays
            min_shape = min(arr.shape for arr in real_array + imaginary_array + phase_array + magnitudes_array)
            imaginary_sum = 0
            real_sum = 0
            mag_sum = 0
            phase_sum = 0


            mag_weights = [
                slider.value()/100 * np.ones(min_shape, dtype=np.float32) if combobox.currentIndex() == 2 else np.zeros(
                    min_shape, dtype=np.float32) for slider, combobox in zip(self.sliders_list, self.combobox_list)]
            phase_weights = [
                slider.value()/100 * np.ones(min_shape, dtype=np.float32) if combobox.currentIndex() == 3 else np.zeros(
                    min_shape, dtype=np.float32) for slider, combobox in zip(self.sliders_list, self.combobox_list)]
            imaginary_weights = [
                slider.value()/100 * np.ones(min_shape, dtype=np.float32) if combobox.currentIndex() == 1 else np.zeros(
                    min_shape, dtype=np.float32) for slider, combobox in zip(self.sliders_list, self.combobox_list)]
            real_weights = [
                slider.value()/100 * np.ones(min_shape, dtype=np.float32) if combobox.currentIndex() == 0 else np.zeros(
                    min_shape, dtype=np.float32) for slider, combobox in zip(self.sliders_list, self.combobox_list)]

            if self.real_imaginary.isChecked():
                for i in range(4):
                    imaginary_sum += imaginary_array[i] * imaginary_weights[i]
                    real_sum += real_array[i] * real_weights[i]
                mixed_image = np.fft.ifft2(np.fft.ifftshift(real_sum + 1j * imaginary_sum))
                final_mixed_image=np.abs(mixed_image).astype(np.uint8)
                if self.output1.isChecked():
                    f.display_output_image(self.output_mixer1, final_mixed_image)
                else:
                    f.display_output_image(self.output_mixer2, final_mixed_image)


            elif self.magnitude_phase.isChecked():
                for i in range(4):
                    mag_sum += magnitudes_array[i] * mag_weights[i]
                    phase_sum += phase_array[i] * phase_weights[i]
                mixed_image = np.fft.ifft2(np.fft.ifftshift(np.multiply(mag_sum, np.exp(1j*phase_sum))))
                cv2.imwrite('test.jpg', np.real(mixed_image))
                final_mixed_image = np.abs(mixed_image).astype(np.uint8)
                if self.output1.isChecked():
                    f.display_output_image(self.output_mixer1, final_mixed_image)
                else:
                    f.display_output_image(self.output_mixer2, final_mixed_image)

            else:
                print("Error: No mixing option selected.")

        except Exception as e:
            print(f"Error during image mixing: {e}")

    def update_combo_box(self):
        for i in range(self.Fourier_comboBox_1.count()):
            self.Fourier_comboBox_1.model().item(i).setEnabled(True)
            self.Fourier_comboBox_2.model().item(i).setEnabled(True)
            self.Fourier_comboBox_3.model().item(i).setEnabled(True)
            self.Fourier_comboBox_4.model().item(i).setEnabled(True)

        if self.real_imaginary.isChecked():
            first_index_to_disable = 2
            second_index_to_disable = 3
            self.toggle_combo_box_options(first_index_to_disable, second_index_to_disable)
            self.Fourier_comboBox_1.setCurrentIndex(0)
            self.Fourier_comboBox_2.setCurrentIndex(0)
            self.Fourier_comboBox_3.setCurrentIndex(0)
            self.Fourier_comboBox_4.setCurrentIndex(0)

        elif self.magnitude_phase.isChecked():
            first_index_to_disable = 0
            second_index_to_disable = 1
            self.toggle_combo_box_options(first_index_to_disable, second_index_to_disable)
            self.Fourier_comboBox_1.setCurrentIndex(2)
            self.Fourier_comboBox_2.setCurrentIndex(2)
            self.Fourier_comboBox_3.setCurrentIndex(2)
            self.Fourier_comboBox_4.setCurrentIndex(2)

    def toggle_combo_box_options(self, first_index_to_disable, second_index_to_disable):
        self.Fourier_comboBox_1.model().item(first_index_to_disable).setEnabled(False)
        self.Fourier_comboBox_2.model().item(first_index_to_disable).setEnabled(False)
        self.Fourier_comboBox_3.model().item(first_index_to_disable).setEnabled(False)
        self.Fourier_comboBox_4.model().item(first_index_to_disable).setEnabled(False)
        self.Fourier_comboBox_1.model().item(second_index_to_disable).setEnabled(False)
        self.Fourier_comboBox_2.model().item(second_index_to_disable).setEnabled(False)
        self.Fourier_comboBox_3.model().item(second_index_to_disable).setEnabled(False)
        self.Fourier_comboBox_4.model().item(second_index_to_disable).setEnabled(False)


def main():
    app = QApplication(sys.argv)

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
