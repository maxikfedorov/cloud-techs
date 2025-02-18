from flask import Flask, request, send_file, jsonify
import cv2
import numpy as np
from io import BytesIO
from effects import EFFECTS  # Ваши фильтры на основе OpenCV

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    try:
        # Получаем данные изображения из запроса
        file = request.data  # Получаем байты изображения из тела запроса
        
        if not file:
            return jsonify({"error": "Файл изображения отсутствует в запросе."}), 400
        
        effect_name = request.args.get('effect', 'blur')  # По умолчанию используем "blur"
        
        if effect_name not in EFFECTS:
            return jsonify({"error": f"Эффект '{effect_name}' не поддерживается."}), 400
        
        # Декодируем изображение из байтов в массив NumPy (OpenCV)
        np_arr = np.frombuffer(file, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if image is None or image.size == 0:
            return jsonify({"error": "Не удалось декодировать изображение. Проверьте формат файла."}), 400
        
        # Применяем выбранный эффект
        processed_image = EFFECTS[effect_name](image)
        
        # Кодируем обработанное изображение обратно в байты
        _, img_encoded = cv2.imencode('.jpg', processed_image)
        img_io = BytesIO(img_encoded.tobytes())
        
        return send_file(img_io, mimetype='image/jpeg')  # Возвращаем изображение в формате JPEG
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
