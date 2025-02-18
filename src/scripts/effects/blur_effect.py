import cv2

def apply_blur(image):
    """Применяет размытие к изображению."""
    return cv2.GaussianBlur(image, (15, 15), 0)
