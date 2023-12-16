import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from os import path
from image import Image
import functions as f
import numpy as np
import cv2

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

        # Signals
        self.button1.clicked.connect(lambda: self.upload(self.image1))
        self.button2.clicked.connect(lambda: self.upload(self.image2))
        self.button3.clicked.connect(lambda: self.upload(self.image3))
        self.button4.clicked.connect(lambda: self.upload(self.image4))

    # Functions

    def upload(self, label):
        filters = "Images (*.jpg *.jpeg *.png);;All Files (*)"
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileNames()", "", filters,
                                                   options=options)

        if file_path:
            # Store file name
            file_name = file_path.split('/')[-1]
            label.setText(file_name)

            # Load images asynchronously
            image = Image(file_path, width=277, height=112)  # Set width and height accordingly
            image.set_image(label)

            # Perform Fourier transform asynchronously
            self.load_fourier_component(image)

    def load_fourier_component(self, image):
        try:
            image_for_fourier = image.read_image()
            real_part, imaginary_part, magnitude_spectrum, phase_spectrum = image.calculate_img_magnitude_phase(
                image_for_fourier)
            f.plot_fourier_component(magnitude_spectrum, real_part, imaginary_part,phase_spectrum,self.Gimage1,2)
        except Exception as e:
            print(f"Error loading Fourier component: {e}")

    def closeEvent(self, event):
        # Release resources when the window is closed
        cv2.destroyAllWindows()


def main():
    app = QApplication(sys.argv)

    # with open("style.qss", "r") as f:
    #     _style = f.read()
    #     app.setStyleSheet(_style)

    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
