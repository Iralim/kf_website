document.addEventListener('DOMContentLoaded', function() {

    // ==========================
    // DOM ELEMENTS
    // ==========================
    const uploadArea = document.getElementById('uploadArea');
    const uploadInput = document.getElementById('imgUpload');
    const uploadTrigger = document.getElementById('uploadTrigger');
    const selectedFilesContainer = document.getElementById('selectedFiles');
    const fileList = document.getElementById('fileList');
    const clearFilesBtn = document.getElementById('clearFiles');

    // ==========================
    // EXISTING FILES
    // ==========================
    let existingFiles = window.existingFiles || [];

    console.log("Полученные existingFiles:", existingFiles);

    function removeFileFromExistingFiles(fileName) {
        const index = existingFiles.indexOf(fileName);
        if (index > -1) {
            existingFiles.splice(index, 1);
            console.log('Файл удален из existingFiles:', fileName);
            console.log('Обновленный existingFiles:', existingFiles);
        }
    }

    // ==========================
    // DELETE PROJECT FUNCTION
    // ==========================
    async function deleteProject(e) {
        const btn = e.target.closest(".delete-project-btn");
        if (!btn) return;

        if (!confirm("Вы уверены, что хотите удалить этот проект?")) return;

        const id = btn.dataset.id;

        try {
            const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            const response = await fetch(`/api/project/${id}`, { 
                method: 'DELETE',
                credentials: 'same-origin',
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
            });
            if (response.ok) {
                btn.closest(".col-md-6.col-lg-4").remove();
            } else {
                alert("Ошибка удаления проекта");
            }
        } catch (err) {
            console.error(err);
            alert("Ошибка при удалении проекта");
        }
    }

    // ==========================
    // FILE UPLOAD FUNCTIONS
    // ==========================
    function validateAndShowFiles() {
        const selectedFiles = Array.from(uploadInput.files);

        if (!selectedFiles.length) {
            selectedFilesContainer.style.display = 'none';
            return;
        }

        // Проверка дубликатов с existingFiles
        const duplicatesWithExisting = selectedFiles.filter(file => existingFiles.includes(file.name));
        if (duplicatesWithExisting.length > 0) {
            alert("Файлы уже существуют:\n" + duplicatesWithExisting.map(f => f.name).join("\n"));
            uploadInput.value = '';
            selectedFilesContainer.style.display = 'none';
            return;
        }

        // Проверка дубликатов внутри новых файлов
        const names = selectedFiles.map(f => f.name);
        const duplicatesInsideUpload = names.filter((name, index) => names.indexOf(name) !== index);
        if (duplicatesInsideUpload.length > 0) {
            alert("Нельзя загружать два файла с одинаковыми именами:\n" + duplicatesInsideUpload.join("\n"));
            uploadInput.value = '';
            selectedFilesContainer.style.display = 'none';
            return;
        }

        // Отображение файлов
        fileList.innerHTML = '';
        selectedFiles.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <div class="flex-grow-1">
                    <div class="fw-medium"><i class="bi bi-file-image text-primary me-2"></i>${file.name}</div>
                    <small class="text-muted">${(file.size / 1024 / 1024).toFixed(2)} MB</small>
                </div>
            `;
            fileList.appendChild(fileItem);
        });
        selectedFilesContainer.style.display = 'block';
    }

    async function safeFetch(url, options = {}) {
        try {
            const response = await fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" }, ...options });
            if (!response.ok) throw new Error("Server error: " + response.status);
            return response;
        } catch (err) {
            console.error(err);
            throw err;
        }
    }

    // ==========================
    // EVENT LISTENERS
    // ==========================
    // 1. Удаление проекта
    document.addEventListener("click", deleteProject);

    // 2. Загрузка файлов по клику на область
    uploadArea.addEventListener('click', e => {
        if (e.target !== uploadTrigger && !uploadTrigger.contains(e.target)) uploadInput.click();
    });
    uploadTrigger.addEventListener('click', e => {
        e.stopPropagation();
        uploadInput.click();
    });

    // 3. Перетаскивание файлов
    uploadArea.addEventListener('dragover', e => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    uploadArea.addEventListener('drop', e => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            uploadInput.files = e.dataTransfer.files;
            validateAndShowFiles();
        }
    });

    // 4. Выбор файлов через диалог
    uploadInput.addEventListener('change', validateAndShowFiles);

    // 5. Очистка списка файлов
    clearFilesBtn.addEventListener('click', () => {
        uploadInput.value = '';
        selectedFilesContainer.style.display = 'none';
        fileList.innerHTML = '';
    });

    // 6. Удаление изображений из галереи
    document.addEventListener("click", async event => {
        const btn = event.target.closest(".delete-btn");
        if (!btn) return;

        const id = btn.dataset.id;
        const item = btn.closest(".gallery-item");
        const img = item.querySelector('img');
        const fileName = img.src.split('/').pop();

        if (!confirm("Удалить изображение?")) return;

        btn.disabled = true;

        try {
            const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            await safeFetch(`/delete_image/${id}`, { 
                method: 'DELETE',
                credentials: 'same-origin',
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
            });
            removeFileFromExistingFiles(fileName);
            item.classList.add("removing");
            setTimeout(() => item.remove(), 300);
        } catch (err) {
            alert("Ошибка удаления");
            btn.disabled = false;
        }
    });

});
