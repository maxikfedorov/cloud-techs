from diffusers import StableDiffusionImg2ImgPipeline
from transformers import DetrImageProcessor, DetrForObjectDetection

def download_models():
    """
    Скачивает необходимые модели для работы скриптов.
    """
    # Скачивание модели Stable Diffusion
    print("Скачивание модели Stable Diffusion...")
    StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    print("Модель Stable Diffusion скачана.")

    # Скачивание модели DETR
    print("Скачивание модели DETR...")
    DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    print("Модель DETR скачана.")

if __name__ == "__main__":
    download_models()
