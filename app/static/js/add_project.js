document.addEventListener("DOMContentLoaded", () => {

    /* ------------------------------------------------------
       Project title uniqueness check
    ------------------------------------------------------ */
    const titleInput = document.querySelector("input[name='title']");
    const msg = document.getElementById("title-check-msg");
    let timer = null;

    if (titleInput) {
        titleInput.addEventListener("input", () => {
            clearTimeout(timer);

            timer = setTimeout(async () => {
                const title = titleInput.value.trim();
                if (!title) {
                    msg.textContent = "";
                    return;
                }

                const response = await fetch(`/check_title?title=${encodeURIComponent(title)}`);
                const data = await response.json();

                msg.innerHTML = data.exists
                    ? "<span class='text-danger'><i class='bi bi-exclamation-circle'></i> A project with this name already exists</span>"
                    : "<span class='text-success'><i class='bi bi-check-circle'></i> Name is available</span>";
            }, 350);
        });
    }

    /* ------------------------------------------------------
       Project deletion
    ------------------------------------------------------ */
    document.addEventListener("click", async (e) => {
        const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const btn = e.target.closest(".delete-project-btn");
        if (!btn) return;

        if (!confirm("Are you sure you want to delete this project?")) return;

        const id = btn.dataset.id;

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
            alert("Error deleting project");
        }
    });

    /* ------------------------------------------------------
       File upload (drag & drop + validation)
    ------------------------------------------------------ */
    const uploadArea = document.getElementById('uploadArea');
    const uploadInput = document.getElementById('imgUpload');
    const uploadTrigger = document.getElementById('uploadTrigger');
    const selectedFilesContainer = document.getElementById('selectedFiles');
    const fileList = document.getElementById('fileList');
    const clearFilesBtn = document.getElementById('clearFiles');

    // Click on zone
    uploadArea.addEventListener('click', function (e) {
        if (e.target !== uploadTrigger && !uploadTrigger.contains(e.target)) {
            uploadInput.click();
        }
    });

    uploadTrigger.addEventListener('click', function (e) {
        e.stopPropagation();
        uploadInput.click();
    });

    // Dragover
    uploadArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function () {
        uploadArea.classList.remove('dragover');
    });

    // Drop
    uploadArea.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        if (e.dataTransfer.files.length) {
            uploadInput.files = e.dataTransfer.files;
            validateAndShowFiles();
        }
    });

    // File selection
    uploadInput.addEventListener('change', validateAndShowFiles);

    // Clear
    clearFilesBtn.addEventListener('click', function () {
        uploadInput.value = '';
        selectedFilesContainer.style.display = 'none';
        fileList.innerHTML = '';
    });

    function validateAndShowFiles() {
        const selectedFiles = Array.from(uploadInput.files);

        if (selectedFiles.length === 0) {
            selectedFilesContainer.style.display = 'none';
            return;
        }

        // Check for duplicates within the same file set
        const names = selectedFiles.map(f => f.name);
        const duplicatesInsideUpload = names.filter((name, index) =>
            names.indexOf(name) !== index
        );

        if (duplicatesInsideUpload.length > 0) {
            alert("Cannot upload two files with the same name:\n" +
                duplicatesInsideUpload.join("\n"));
            uploadInput.value = "";
            selectedFilesContainer.style.display = 'none';
            return;
        }

        // Display file list
        fileList.innerHTML = '';
        selectedFiles.forEach((file) => {
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
});