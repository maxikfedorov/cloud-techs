import cv2
import numpy as np

def apply_warm_filter(image):
    """Добавляет теплый эффект к изображению."""
    # Увеличиваем красный канал
    increase_red = np.full_like(image[:, :, 2], 30)
    image[:, :, 2] = cv2.add(image[:, :, 2], increase_red)

    # Увеличиваем зелёный канал (немного)
    increase_green = np.full_like(image[:, :, 1], 15)
    image[:, :, 1] = cv2.add(image[:, :, 1], increase_green)

    # Уменьшаем синий канал
    decrease_blue = np.full_like(image[:, :, 0], 20)
    image[:, :, 0] = cv2.subtract(image[:, :, 0], decrease_blue)

    return image
