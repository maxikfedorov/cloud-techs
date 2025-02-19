import cv2
import numpy as np
from ultralytics import YOLO

# Загрузка модели YOLOv8 с вашими весами
MODEL_PATH = "../../models/yolo8n_signs.pt"
model = YOLO(MODEL_PATH)

def apply_yolo(image: np.ndarray) -> np.ndarray:
    """
    Применяет модель YOLOv8 для детекции объектов на изображении и возвращает обработанное изображение.

    :param image: Исходное изображение в формате NumPy (OpenCV).
    :return: Изображение с аннотациями в формате NumPy (OpenCV).
    """
    # Выполнение предсказания
    results = model.predict(source=image, save=False, conf=0.25)
    
    # Получаем аннотированное изображение
    annotated_image = results[0].plot()

    return annotated_image