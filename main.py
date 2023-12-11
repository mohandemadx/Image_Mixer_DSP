import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, uic
from image import ImageDisplayWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI from the .ui file
        uic.loadUi('main_window.ui', self)

        # Create an instance of ImageDisplayWidget
        self.image_widget = ImageDisplayWidget(self)

        # Set up layout for the main window
        main_layout = QVBoxLayout(self.centralWidget())
        main_layout.addWidget(self.image_widget)

        # Connect UI signals and slots as needed

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
