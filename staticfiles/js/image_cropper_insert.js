document.addEventListener('DOMContentLoaded', function () {
    const insertButton = document.getElementById('custom-insert-image');
    const fileInput = document.getElementById('custom-image-input');
    const preview = document.getElementById('image-preview');
    const cropContainer = document.getElementById('image-crop-container');
    const cropConfirm = document.getElementById('crop-confirm');

    let cropper;


    // 2. Trigger file selection
    insertButton.addEventListener('click', () => {
        fileInput.click();
    });

    // 3. Show cropper on file selected
    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (event) {
            preview.src = event.target.result;
            cropContainer.style.display = 'block';

            if (cropper) cropper.destroy();
            cropper = new Cropper(preview, {
                //aspectRatio: 1,
                viewMode: 1,
            });
        };
        reader.readAsDataURL(file);
    });

    // 4. Crop, upload to Cloudinary, insert image
    cropConfirm.addEventListener('click', function () {
        if (!editorInstance) {
            alert("Editor not ready yet.");
            return;
        }
        const canvas = cropper.getCroppedCanvas({ width: 500, height: 500 });

        canvas.toBlob(function (blob) {
            const formData = new FormData();
            formData.append('file', blob, 'cropped.jpg');
            formData.append('upload_preset', 'ckeditor_uploads');

            fetch('https://api.cloudinary.com/v1_1/shamelesis/image/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const imageUrl = data.secure_url;

                editorInstance.model.change(writer => {
                    const imageElement = writer.createElement('imageBlock', {
                        src: imageUrl,
                        alt: 'Cropped Image',
                    });

                    editorInstance.model.insertContent(imageElement, editorInstance.model.document.selection);
                });

                // Reset UI
                cropContainer.style.display = 'none';
                fileInput.value = '';
                cropper.destroy();
            })
            .catch(err => {
                console.error('Upload failed:', err);
            });
        }, 'image/jpeg', 0.9);
    });
});