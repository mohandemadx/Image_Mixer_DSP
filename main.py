import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from clickableLabel import QClickableLabel
from PyQt5.uic import loadUiType
from os import path
import image as Im
import functions as f

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
        # self.image = QClickableLabel('', self.image1)
        # self.image.mouseDoubleClickEvent = self.upload(self.filters, self.label1)
        
        
        
    # Functions
    
    def upload(self, filters, label):
        # General Function kan mfrood n3mlhaa mn sana bdl m7na bn3ml wa7da gdeeda kol mara
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileNames()", "", filters, options=options)
        
        if file_path:
            # Store file name
            file_name = file_path.split('/')[-1]
            label.setText(file_name)
            
            image = Im.read_image(file_path)



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