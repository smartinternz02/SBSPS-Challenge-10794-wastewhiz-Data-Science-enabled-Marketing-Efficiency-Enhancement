document.addEventListener("DOMContentLoaded", function () {
    // This event listener ensures that the code runs after the HTML document is fully loaded.

    const dropArea = document.getElementById("drop-area");
    const fileInput = document.querySelector("input[name='file']");
    const uploadButton = document.querySelector(".upload-button");
    const cannotUploadMessage = document.querySelector(".cannot-upload-message");
    const uploadedFile = document.querySelector(".file-block");
    const fileName = document.querySelector(".file-name");
    const fileSize = document.querySelector(".file-size");
    const progressBar = document.querySelector(".progress-bar");
    const removeFileButton = document.querySelector(".remove-file-icon");
    let fileFlag = 0;
    
    // Grab various DOM elements and initialize some variables for later use.

    dropArea.addEventListener("dragenter", (event) => {
        event.preventDefault();
        dropArea.style.border = "2px dashed #292929";
    });

    dropArea.addEventListener("dragleave", (event) => {
        event.preventDefault();
        dropArea.style.border = "2px dashed #ccc";
    });

    // These event listeners handle the visual feedback when a file is dragged over the drop area.
    // The border of the drop area changes to indicate the area where a file can be dropped.

    dropArea.addEventListener("dragover", (event) => {
        event.preventDefault();
    });

    // This event listener prevents the default browser behavior when a file is dragged over the drop area.

    dropArea.addEventListener("drop", (event) => {
        event.preventDefault();
        dropArea.style.border = "2px dashed #ccc";

        const file = event.dataTransfer.files[0];
        if (file) {
            fileInput.files = event.dataTransfer.files;
            fileName.textContent = file.name;
            fileSize.textContent = (file.size / 1024).toFixed(1) + " KB";
            uploadedFile.style.display = "flex";
            progressBar.style.width = "0";
            fileFlag = 0;
        }
    });

    // This event listener handles the actual file dropping.
    // When a file is dropped, it updates the file input and displays the file details.

    uploadButton.addEventListener("click", () => {
        let isFileUploaded = fileInput.value;
        if (isFileUploaded !== "") {
            if (fileFlag === 0) {
                // This part of the code simulates a progress bar animation.
            }
        } else {
            cannotUploadMessage.style.display = "flex";
        }
    });

    // This event listener is triggered when the "Upload" button is clicked.
    // It checks if a file has been selected and simulates a progress bar animation if a file is being uploaded.

    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        if (file) {
            fileName.textContent = file.name;
            fileSize.textContent = (file.size / 1024).toFixed(1) + " KB";
            uploadedFile.style.display = "flex";
            progressBar.style.width = "0";
            fileFlag = 0;
        }
    });

    // This event listener triggers when the file input's value changes (a file is selected).
    // It updates the file details and displays them.

    removeFileButton.addEventListener("click", () => {
        fileInput.value = "";
        fileName.textContent = "";
        fileSize.textContent = "";
        uploadedFile.style.display = "none";
        fileFlag = 0;
    });

    // This event listener is triggered when the "Remove" button is clicked.
    // It resets the file input and hides the file details.

    function showUploadedMessage(fileName) {
        const uploadedMessageContainer = document.createElement("div");
        uploadedMessageContainer.classList.add("uploaded-message-container");
    
        const uploadedFileName = document.createElement("p");
        uploadedFileName.textContent = `File "${fileName}" has been uploaded!`;
        uploadedFileName.classList.add("uploaded-file-name");
        
        const removeButton = document.createElement("button");
        removeButton.textContent = "Remove";
        removeButton.classList.add("remove-button");
    
        uploadedMessageContainer.appendChild(uploadedFileName);
        uploadedMessageContainer.appendChild(removeButton);
        uploadedFile.appendChild(uploadedMessageContainer);
    
        removeButton.addEventListener("click", () => {
            uploadedMessageContainer.remove();
            deleteUploadedFile();
        });
    
        setTimeout(() => {
            uploadedMessageContainer.remove();
        }, 3000);
    }
    // Function to display a message when the file has been uploaded.

    function deleteUploadedFile() {
        fileInput.value = "";
        fileName.textContent = "";
        fileSize.textContent = "";
        uploadedFile.style.display = "none";
        progressBar.style.width = "0";
        fileFlag = 0;
    }

    uploadButton.addEventListener("click", () => {
        let isFileUploaded = fileInput.value;
        if (isFileUploaded !== "") {
            if (fileFlag === 0) {
                fileFlag = 1;
                var width = 0;
                var id = setInterval(frame, 50);
                function frame() {
                    if (width >= 390) {
                        clearInterval(id);
                        uploadButton.innerHTML = `<span class="material-icons-outlined upload-button-icon"> check_circle </span> Uploaded`;
                        const uploadedFileName = fileInput.files[0].name;
                        showUploadedMessage(uploadedFileName);
                    } else {
                        width += 5;
                        progressBar.style.width = width + "px";
                    }
                }
            }
        } else {
            cannotUploadMessage.style.display = "flex";
        }
    });

    removeFileButton.addEventListener("click", () => {
        deleteUploadedFile();
    });

});

