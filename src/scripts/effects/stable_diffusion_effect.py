from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import numpy as np
import cv2

PROMPT = """
    A breathtaking anime-style illustration of a vibrant fantasy city at sunset, 
    with glowing neon lights, cherry blossom petals gently falling in the wind, 
    a beautiful anime girl with flowing hair and expressive eyes standing on a bridge, 
    wearing a detailed kimono with intricate patterns, surrounded by magical sparkles 
    and a dreamy atmosphere. Ultra-detailed, dynamic lighting, cinematic composition, 
    Studio Ghibli and Makoto Shinkai inspired.
    """

def apply_stable_diffusion(image: np.ndarray, prompt=PROMPT, strength=0.5, guidance_scale=7.5) -> np.ndarray:
    """
    Применяет эффект Stable Diffusion к изображению и возвращает результат в формате OpenCV (NumPy).
    
    :param image: Исходное изображение в формате NumPy (OpenCV).
    :param prompt: Текстовый запрос для генерации эффекта.
    :param strength: Сила применения эффекта (0-1).
    :param guidance_scale: Масштаб управления стилем.
    :return: Обработанное изображение в формате NumPy (OpenCV).
    """
    # Сохраняем исходные размеры изображения
    original_height, original_width = image.shape[:2]

    # Преобразуем изображение из NumPy в PIL.Image
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Загружаем модель Stable Diffusion
    pipeline = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipeline.to("cuda")  # Используем GPU, если доступно

    # Изменяем размер изображения до 512x512 (требование модели)
    resized_image = pil_image.convert("RGB").resize((512, 512))

    # Применяем текстовый prompt через модель
    result = pipeline(
        prompt=prompt,
        image=resized_image,
        strength=strength,
        guidance_scale=guidance_scale
    ).images[0]

    # Масштабируем результат обратно к исходным размерам
    result_resized = result.resize((original_width, original_height), Image.LANCZOS)

    # Преобразуем результат из PIL.Image обратно в NumPy (OpenCV)
    result_np = cv2.cvtColor(np.array(result_resized), cv2.COLOR_RGB2BGR)

    return result_np
