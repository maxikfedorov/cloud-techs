document.addEventListener('DOMContentLoaded', async () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const uploadStatus = document.getElementById('uploadStatus');
    const galleryButton = document.createElement('button');
    galleryButton.className = 'btn btn-secondary btn-lg w-100 mt-3';
    galleryButton.textContent = 'Выбрать из галереи';
    uploadForm.insertBefore(galleryButton, uploadForm.querySelector('button[type="submit"]'));

    const modal = new bootstrap.Modal(document.getElementById('imageGalleryModal'));
    const imageGalleryGrid = document.getElementById('imageGalleryGrid');

    // Загрузка изображений из БД в галерею
    async function loadImagesFromDB() {
        try {
            const response = await fetch('/images');
            if (!response.ok) throw new Error('Ошибка загрузки изображений');
            const images = await response.json();

            imageGalleryGrid.innerHTML = ''; // Очищаем сетку перед добавлением новых изображений
            images.forEach(image => {
                const imageCard = document.createElement('div');
                imageCard.className = 'col';
                imageCard.innerHTML = `
                    <div class="card h-100 shadow-sm">
                        <img src="/image/${image._id}" class="card-img-top" alt="${image.name}" style="height: 200px; object-fit: cover;">
                        <div class="card-body text-center">
                            <p class="card-text text-truncate">${image.name}</p>
                            <button class="btn btn-primary btn-sm select-image" data-image-id="${image._id}">
                                Выбрать
                            </button>
                        </div>
                    </div>
                `;
                imageGalleryGrid.appendChild(imageCard);
            });
        } catch (error) {
            console.error('Ошибка загрузки изображений:', error);
        }
    }

    // Обработчик кнопки "Выбрать из галереи"
    galleryButton.addEventListener('click', async (e) => {
        e.preventDefault();
        await loadImagesFromDB();
        modal.show();
    });


    // Обработчик выбора изображения из галереи
    imageGalleryGrid.addEventListener('click', async (e) => {
        if (e.target.classList.contains('select-image')) {
            const imageId = e.target.dataset.imageId;
            const imageName = e.target.closest('.card').querySelector('.card-text').textContent;

            try {
                // Отображаем название выбранного изображения в зоне dropZone
                dropZone.textContent = `Выбрано изображение: ${imageName}`;
                dropZone.classList.add('file-selected');
                dropZone.dataset.selectedImageId = imageId; // Сохраняем ID выбранного изображения для дальнейшей обработки

                enableProcessButton(); // Активируем кнопку "Обработать"
                modal.hide(); // Закрываем модальное окно
            } catch (error) {
                console.error('Ошибка отображения изображения:', error);
            }
            enableProcessButton();
        }
    });


    // Клик по зоне для выбора файла
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Перетаскивание файла над зоной
    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropZone.classList.add('drag-over');
        dropZone.textContent = 'Отпустите файл для загрузки';
    });

    // Уход мыши из зоны перетаскивания
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
        resetDropZoneText();
    });

    // Бросок файла в зону
    dropZone.addEventListener('drop', (event) => {
        event.preventDefault();
        dropZone.classList.remove('drag-over');
        fileInput.files = event.dataTransfer.files;

        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            dropZone.textContent = `Выбран файл: ${file.name}`;
            dropZone.classList.add('file-selected');
            enableProcessButton(); // Активируем кнопку "Обработать"
        }
    });

    function resetDropZone() {
        dropZone.style.backgroundImage = '';
        dropZone.style.backgroundSize = '';
        dropZone.style.backgroundPosition = '';
        dropZone.textContent = 'Перетащите файл сюда или нажмите для выбора.';
        delete dropZone.dataset.selectedImageId; // Удаляем сохранённый ID изображения
    }


    // Отображение имени файла после выбора
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            showFileName(fileInput.files[0]);
            enableProcessButton(); // Активируем кнопку "Обработать"
        }
    });


    // Функция отображения имени файла
    function showFileName(file) {
        dropZone.textContent = `Выбран файл: ${file.name}`;
        dropZone.classList.add('file-selected');
    }

    async function displayUploadedImages(originalImageId, processedImageId) {
        // Отображаем исходное изображение
        const originalImage = document.getElementById('originalImage');
        originalImage.src = `/image/${originalImageId}`;
        originalImage.style.display = 'block';

        // Отображаем обработанное изображение
        const processedImage = document.getElementById('processedImage');
        processedImage.src = `/image/${processedImageId}`;
        processedImage.style.display = 'block';
    }

    // Обновляем обработчик формы
    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(uploadForm);

        // Получаем выбранный эффект из выпадающего меню
        const effectSelect = document.getElementById('effectSelect');
        const selectedEffect = effectSelect.value;

        uploadStatus.textContent = 'Загрузка...';
        uploadStatus.className = 'text-info';

        try {
            // Отправляем запрос на сервер с выбранным эффектом
            const response = await fetch(`/upload?effect=${selectedEffect}`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                uploadStatus.textContent = 'Изображение успешно загружено!';
                uploadStatus.className = 'text-success';

                // Отобразить исходное и обработанное изображения
                displayUploadedImages(data.originalImageId, data.processedImageId);
            } else {
                throw new Error('Ошибка загрузки изображения');
            }
        } catch (error) {
            console.error(error);
            uploadStatus.textContent = 'Ошибка загрузки изображения.';
            uploadStatus.className = 'text-danger';
        }
    });

    function resetDropZoneText() {
        dropZone.textContent = 'Перетащите файл сюда или нажмите для выбора.';
    }

    // Загрузка списка эффектов при старте страницы
    async function loadEffects() {
        try {
            const effectSelect = document.getElementById('effectSelect');
            const response = await fetch('/effects');
            if (!response.ok) throw new Error('Ошибка загрузки эффектов');

            const effects = await response.json();
            effectSelect.innerHTML = '';
            effects.forEach(effect => {
                const option = document.createElement('option');
                option.value = effect.key;
                option.textContent = effect.name;
                effectSelect.appendChild(option);
            });
        } catch (error) {
            console.error(error);
        }
    }

    const processButton = document.createElement('button');
    processButton.textContent = 'Обработать из БД';
    processButton.className = 'btn btn-primary mt-3';
    processButton.disabled = true; // Делаем кнопку неактивной по умолчанию
    uploadForm.appendChild(processButton);

    // Активируем кнопку после выбора изображения
    function enableProcessButton() {
        processButton.disabled = false;
    }

    // Обработчик кнопки "Обработать"
    processButton.addEventListener('click', async () => {
        const selectedImageId = dropZone.dataset.selectedImageId; // Получаем ID выбранного изображения
        const effectSelect = document.getElementById('effectSelect');
        const selectedEffect = effectSelect.value;

        if (!selectedImageId) {
            uploadStatus.textContent = 'Выберите изображение перед обработкой.';
            uploadStatus.className = 'text-danger';
            return;
        }

        uploadStatus.textContent = 'Обработка...';
        uploadStatus.className = 'text-info';

        try {
            const response = await fetch(`/process-db-image/${selectedImageId}?effect=${selectedEffect}`, {
                method: 'POST',
            });

            if (response.ok) {
                const data = await response.json();
                displayUploadedImages(selectedImageId, data.processedImageId);
                uploadStatus.textContent = 'Изображение успешно обработано!';
                uploadStatus.className = 'text-success';
            } else {
                throw new Error('Ошибка обработки изображения');
            }
        } catch (error) {
            console.error('Ошибка обработки:', error);
            uploadStatus.textContent = 'Ошибка обработки.';
            uploadStatus.className = 'text-danger';
        }
    });

    await loadEffects(); // Загружаем эффекты при загрузке страницы
});
