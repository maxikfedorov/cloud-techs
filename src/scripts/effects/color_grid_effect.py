import cv2
import random
import numpy as np

def apply_color_grid(image):
    """
    Применяет 4 разных случайных фильтра к копиям изображения,
    объединяет их в одно изображение и масштабирует к размеру исходного.
    """
    # Доступные цветовые пространства (фильтры)
    color_spaces = [
        cv2.COLOR_BGR2GRAY,  # Оттенки серого
        cv2.COLOR_BGR2HSV,   # Hue-Saturation-Value
        cv2.COLOR_BGR2LAB,   # LAB color space
        cv2.COLOR_BGR2LUV,   # LUV color space
        cv2.COLOR_BGR2XYZ,   # CIE 1931 XYZ color space
        cv2.COLOR_BGR2YCrCb, # YCrCb color space
        cv2.COLOR_BGR2HLS    # Hue-Lightness-Saturation
    ]
    
    # Выбираем 4 случайных фильтра без повторений
    selected_filters = random.sample(color_spaces, 4)
    
    # Применяем каждый фильтр к копии изображения
    transformed_images = []
    for filter_type in selected_filters:
        transformed_image = cv2.cvtColor(image, filter_type)
        
        # Если результат в оттенках серого, конвертируем обратно в BGR для объединения
        if len(transformed_image.shape) == 2:  # Проверка на grayscale
            transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_GRAY2BGR)
        
        transformed_images.append(transformed_image)
    
    # Объединяем изображения в коллаж (2x2)
    top_row = np.hstack((transformed_images[0], transformed_images[1]))
    bottom_row = np.hstack((transformed_images[2], transformed_images[3]))
    combined_image = np.vstack((top_row, bottom_row))
    
    # Масштабируем итоговое изображение до размера исходного
    final_image = cv2.resize(combined_image, (image.shape[1], image.shape[0]))
    
    return final_image