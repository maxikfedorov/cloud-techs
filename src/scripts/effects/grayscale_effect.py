import cv2

def apply_grayscale(image):
    """Преобразует изображение в оттенки серого."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
