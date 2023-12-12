from clickableLabel import QClickableLabel
from PyQt5.QtWidgets import QLabel

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