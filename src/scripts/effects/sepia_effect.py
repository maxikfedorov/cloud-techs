import cv2
import numpy as np

def apply_sepia(image):
    """Применяет эффект сепии к изображению."""
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    return cv2.transform(image, kernel)
