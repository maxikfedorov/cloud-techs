from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image, ImageDraw, ImageFont
import torch
import numpy as np
import cv2
from typing import Union, Tuple


def apply_object_detection(
    image: np.ndarray,
    confidence_threshold: float = 0.7,
    font_size: int = 64,
    box_width: int = 3
) -> np.ndarray:
    """
    Обрабатывает изображение, детектирует объекты и возвращает обработанное изображение.
    
    Args:
        image (np.ndarray): Изображение в формате NumPy (OpenCV).
        confidence_threshold (float): Порог уверенности для детекции (0-1).
        font_size (int): Размер шрифта для подписей.
        box_width (int): Толщина рамки бокса.
    
    Returns:
        np.ndarray: Обработанное изображение в формате NumPy (OpenCV).
    """
    
    def draw_fancy_box(
        draw: ImageDraw.ImageDraw,
        box: Tuple[int, int, int, int],
        label: str,
        score: float,
        color: Tuple[int, int, int]
    ) -> None:
        """Отрисовка стильного бокса с подписью"""
        # Рисуем основной прямоугольник
        draw.rectangle(box, outline=color, width=box_width)
        
        # Подготовка текста и шрифта
        label_text = f"{label}: {score:.2f}"
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Получаем размеры текста
        text_bbox = draw.textbbox((0, 0), label_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Рисуем фон для текста
        text_bg = [box[0], box[1] - text_height - 10,
                  box[0] + text_width + 10, box[1]]
        draw.rectangle(text_bg, fill=color)
        
        # Пишем текст
        draw.text((box[0] + 5, box[1] - text_height - 5),
                 label_text, fill='white', font=font)

    def generate_color(label: str) -> Tuple[int, int, int]:
        """Генерация уникального цвета для класса"""
        np.random.seed(hash(label) % 2**32)
        return tuple(map(int, np.random.randint(0, 255, size=3)))

    # Преобразуем изображение из NumPy в PIL.Image
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Инициализация модели и процессора
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    model.eval()

    # Обработка изображения через модель DETR
    inputs = processor(images=pil_image, return_tensors="pt")
    outputs = model(**inputs)

    # Получение результатов детекции
    target_sizes = torch.tensor([pil_image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs, target_sizes=target_sizes)[0]

    # Подготовка к отрисовке
    image_draw = pil_image.copy()
    draw = ImageDraw.Draw(image_draw)
    class_colors = {}

    # Отрисовка результатов детекции объектов
    detected_objects = 0
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        score_value = score.item()
        if score_value > confidence_threshold:
            detected_objects += 1
            box = [round(i) for i in box.tolist()]
            label_text = model.config.id2label[label.item()]
            
            # Получаем или генерируем цвет для класса
            if label_text not in class_colors:
                class_colors[label_text] = generate_color(label_text)
            
            # Отрисовка бокса с подписью
            draw_fancy_box(draw, box, label_text,
                         score_value, class_colors[label_text])

    # Добавление информации о количестве объектов на изображении
    try:
        font = ImageFont.truetype("arial.ttf", font_size + 4)
    except:
        font = ImageFont.load_default()
        
    info_text = f"Detected objects: {detected_objects}"
    draw.text((10, 10), info_text, fill='white',
              font=font, stroke_width=2, stroke_fill='black')

    # Преобразуем обработанное изображение обратно в формат NumPy (OpenCV)
    result_np = cv2.cvtColor(np.array(image_draw), cv2.COLOR_RGB2BGR)

    return result_np
