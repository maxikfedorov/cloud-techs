const express = require('express');
const path = require('path');
const cors = require('cors');
const morgan = require('morgan');
const multer = require('multer');
const { connectDB, Image } = require('./db');
const axios = require('axios'); 

require('dotenv').config();

const app = express();
const PORT = 3000;

// Список доступных эффектов
const EFFECTS = [
    { key: 'blur', name: 'Размытие' },
    { key: 'grayscale', name: 'Оттенки серого' },
    { key: 'edges', name: 'Обнаружение краёв' },
    { key: 'sepia', name: 'Сепия' },
    { key: 'inversion', name: 'Инверсия цветов' }, 
    { key: 'blue_boost', name: 'Усиление синего' }, 
    { key: 'warm_filter', name: 'Тёплый фильтр' }, 
    { key: 'stable_diffusion', name: 'Stable Diffusion' },
    { key: 'object_detection', name: 'Детекция объектов' },
    { key: 'detection_yolo', name: 'Детекция знаков' },
    { key: 'color_grid', name: 'Цветовая сетка' }

];

// Подключение к базе данных
connectDB();

// Настройка multer для обработки файлов
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Middleware
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Указываем путь к статическим файлам
app.use(express.static(path.join(__dirname, '../public')));

// Главная страница
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'index.html'));
});

app.post('/upload', upload.single('image'), async (req, res) => {
    try {
        const { buffer, mimetype, originalname } = req.file;

        // Получаем выбранный эффект из параметров запроса
        const effect = req.query.effect || 'blur'; // По умолчанию "blur"

        // Сохраняем исходное изображение в базу данных
        const originalImage = new Image({
            name: originalname,
            data: buffer,
            contentType: mimetype,
        });
        await originalImage.save();

        // Отправляем на Flask-сервер для обработки с выбранным эффектом
        const flaskResponse = await axios.post(`http://127.0.0.1:5000/process?effect=${effect}`, buffer, {
            headers: {
                'Content-Type': mimetype,
            },
            responseType: 'arraybuffer',
        });

        // Сохраняем обработанное изображение в базу данных
        const processedImage = new Image({
            name: `processed_${originalname}`,
            data: flaskResponse.data,
            contentType: mimetype,
        });
        await processedImage.save();

        res.status(200).json({ 
            message: 'Изображение успешно обработано!', 
            originalImageId: originalImage._id,
            processedImageId: processedImage._id 
        });
    } catch (error) {
        console.error(error);
        res.status(500).send('Ошибка при обработке изображения.');
    }
});

// Эндпоинт для получения списка изображений
app.get('/images', async (req, res) => {
    try {
        const images = await Image.find({}, '_id name'); // Получаем только ID и имя файла
        res.status(200).json(images);
    } catch (error) {
        console.error(error);
        res.status(500).send('Ошибка при получении списка изображений.');
    }
});

// Эндпоинт для получения изображения из базы данных
app.get('/image/:id', async (req, res) => {
    try {
        const image = await Image.findById(req.params.id);
        if (!image) {
            return res.status(404).send('Изображение не найдено.');
        }
        res.set('Content-Type', image.contentType);
        res.send(image.data);
    } catch (error) {
        console.error(error);
        res.status(500).send('Ошибка при получении изображения.');
    }
});

// Эндпоинт для получения списка эффектов
app.get('/effects', (req, res) => {
    res.status(200).json(EFFECTS);
});

// Эндпоинт для обработки изображения из БД
app.post('/process-db-image/:id', async (req, res) => {
    try {
        const originalImage = await Image.findById(req.params.id);
        const effect = req.query.effect || 'blur';

        const flaskResponse = await axios.post(
            `http://127.0.0.1:5000/process?effect=${effect}`,
            originalImage.data,
            {
                headers: {
                    'Content-Type': originalImage.contentType
                },
                responseType: 'arraybuffer'
            }
        );

        const processedImage = new Image({
            name: `processed_${originalImage.name}`,
            data: flaskResponse.data,
            contentType: originalImage.contentType
        });
        await processedImage.save();

        res.status(200).json({
            message: 'Изображение успешно обработано!',
            processedImageId: processedImage._id
        });
    } catch (error) {
        console.error(error);
        res.status(500).send('Ошибка при обработке изображения.');
    }
});

// Запуск сервера
app.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});
