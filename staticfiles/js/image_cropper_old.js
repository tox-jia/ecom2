document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('input[name="image"]');
    if (!input) return;

    const preview = document.createElement('img');
    preview.style.maxWidth = '100%';
    preview.style.marginTop = '10px';
    const container = document.createElement('div');
    container.style.marginTop = '20px';
    input.parentNode.appendChild(container);
    container.appendChild(preview);

    let cropper;

    input.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (event) {
            preview.src = event.target.result;

            if (cropper) cropper.destroy();

            cropper = new Cropper(preview, {
                aspectRatio: 1,
                viewMode: 1,
                autoCropArea: 1,
                cropend() {
                    const croppedCanvas = cropper.getCroppedCanvas({
                        width: 800,
                        height: 800,
                    });

                    croppedCanvas.toBlob(blob => {
                        const newFile = new File([blob], "cropped.jpg", { type: "image/jpeg" });
                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(newFile);
                        input.files = dataTransfer.files;
                    }, "image/jpeg", 0.9);
                }
            });
        };
        reader.readAsDataURL(file);
    });
});