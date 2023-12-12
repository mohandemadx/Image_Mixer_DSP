from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QFileDialog, QWidget
from PyQt5.QtCore import Qt

class DoubleClickableLabel(QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.upload_file()

    def upload_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            print(f"Selected File: {file_path}")
            # Add your file handling logic here

class FileUploadApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()

        layout = QVBoxLayout(central_widget)

        # Create a double-clickable label
        self.double_click_label = DoubleClickableLabel("Double-Click to Upload")
        layout.addWidget(self.double_click_label)

        # Add a button to demonstrate that other widgets are still clickable
        button = QPushButton("Click Me")
        button.clicked.connect(self.button_clicked)
        layout.addWidget(button)

        self.setCentralWidget(central_widget)

        self.setWindowTitle('File Upload App')
        self.setGeometry(100, 100, 400, 300)

    def button_clicked(self):
        print("Button Clicked!")

if __name__ == '__main__':
    app = QApplication([])
    window = FileUploadApp()
    window.show()
    app.exec_()
