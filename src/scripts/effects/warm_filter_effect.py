import cv2
import numpy as np

def apply_warm_filter(image):
    """Добавляет теплый эффект к изображению."""
    increase_red = np.full_like(image[:, :, 2], 30)
    increase_green = np.full_like(image[:, :, 1], -10)
    
    image[:, :, 2] = cv2.add(image[:, :, 2], increase_red) # Увеличение красного
    image[:, :, 1] = cv2.add(image[:, :, 1], increase_green) # Уменьшение зеленого
    
    return image
