import cv2

def apply_inversion(image):
    """Инвертирует цвета изображения."""
    return cv2.bitwise_not(image)
