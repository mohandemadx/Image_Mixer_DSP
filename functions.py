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

def plot_fourier_component(real_part, imaginary_part, magnitude_spectrum, phase_spectrum ,label, index=3):
    if index == 0:
        q_img = self.numpy_to_qpixmap(real_part)
        label.setPixmap(q_img)
        label.setScaledContents(True)
        label.setWindowTitle('Real Part')
    elif index == 1:
        q_img = self.numpy_to_qpixmap(imaginary_part)
        label.setPixmap(q_img)
        label.setScaledContents(True)
        label.setWindowTitle('Imaginary Part')
    elif index == 2:
        q_img = self.numpy_to_qpixmap(phase_spectrum)
        label.setPixmap(q_img)
        label.setScaledContents(True)
        label.setWindowTitle('Phase Spectrum')
    else:
        # Ensure magnitude_spectrum is not modified in-place
        magnitude_spectrum = np.log1p(np.clip(magnitude_spectrum, 0, None).copy())

        # Check for NaN values and replace with a default value
        if np.isnan(np.sum(magnitude_spectrum)):
            print("Warning: Invalid values encountered in magnitude_spectrum. Replacing with zeros.")
            magnitude_spectrum = np.zeros_like(magnitude_spectrum)

            # Convert NumPy array to QPixmap for display
        q_img = numpy_to_qpixmap(magnitude_spectrum)
        label.setPixmap(q_img)
        label.setScaledContents(True)
        label.setWindowTitle('Magnitude Spectrum')


def numpy_to_qpixmap(numpy_array):
    # Check for NaN values in numpy_array
    if np.isnan(np.sum(numpy_array)):
        print("Warning: NaN values encountered in numpy_array. Replacing with zeros.")
        numpy_array[np.isnan(numpy_array)] = 0

    # Ensure the array is normalized to the range [0, 255], avoiding division by zero
    min_val = numpy_array.min()
    max_val = numpy_array.max()

    if min_val == max_val:
        # Handle the case where min_val and max_val are equal
        print("Warning: min_val and max_val are equal. Avoiding division by zero.")
        normalized_array = numpy_array.copy()
    else:
        # Clip values to avoid negative values before taking the logarithm
        numpy_array_clipped = np.clip(numpy_array, 0, None)
        normalized_array = ((numpy_array_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

    height, width = normalized_array.shape[:2]

    # Convert NumPy array to QImage
    q_image = QImage(normalized_array.data, width, height, normalized_array.strides[0], QImage.Format_Grayscale8)

    # Convert QImage to QPixmap
    q_pixmap = QPixmap.fromImage(q_image)

    return q_pixmap