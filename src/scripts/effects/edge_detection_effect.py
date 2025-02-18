import cv2

def apply_edges(image):
    """Применяет фильтр для выделения границ."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 100, 200)
