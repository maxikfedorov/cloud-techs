// db.js
const mongoose = require('mongoose');

// Подключение к MongoDB
const connectDB = async () => {
    try {
        await mongoose.connect(process.env.MONGODB_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        console.log('Подключение к MongoDB успешно');
    } catch (error) {
        console.error('Ошибка подключения к MongoDB:', error.message);
        process.exit(1);
    }
};

// Определение схемы для хранения изображений
const imageSchema = new mongoose.Schema({
    name: { type: String, required: true },
    data: { type: Buffer, required: true },
    contentType: { type: String, required: true },
});

const Image = mongoose.model('Image', imageSchema);

module.exports = { connectDB, Image };
