import cv2
import numpy as np

def apply_blue_boost(image):
    """Увеличивает интенсивность синего цвета."""
    blue_channel = image[:, :, 0]
    blue_channel = cv2.add(blue_channel, 50)
    image[:, :, 0] = blue_channel
    return image
