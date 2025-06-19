//console.log("imagecropupload plugin loaded");
//
//CKEDITOR.plugins.add('imagecropupload', {
//    icons: 'imagecropupload',
//    init: function (editor) {
//        editor.addCommand('openCropDialog', {
//            exec: function () {
//                // You can open a file input and attach Cropper.js logic here
//                alert("Image crop dialog would open here.");
//            }
//        });
//        editor.ui.addButton('ImageCropUpload', {
//            label: 'Upload Cropped Image',
//            command: 'openCropDialog',
//            toolbar: 'insert',
//            icon: '/static/icons/crop-upload-icon.png'
//        });
//    }
//});


//CKEDITOR.plugins.add('imagecropupload', {
//    icons: 'imagecropupload',
//    init: function (editor) {
//        editor.addCommand('openCropDialog', {
//            exec: function () {
//                const input = document.createElement('input');
//                input.type = 'file';
//                input.accept = 'image/*';
//                input.style.display = 'none';
//
//                input.addEventListener('change', async function () {
//                    const file = input.files[0];
//                    if (!file) return;
//
//                    // Show cropping modal
//                    const reader = new FileReader();
//                    reader.onload = function (e) {
//                        const imageData = e.target.result;
//
//                        // Open modal with Cropper.js (you'll need to build this part)
//                        openCropperModal(imageData, async function (croppedBlob) {
//                            // Upload to Cloudinary
//                            const formData = new FormData();
//                            formData.append('file', croppedBlob);
//                            formData.append('upload_preset', 'your_unsigned_preset');
//
//                            const res = await fetch('https://api.cloudinary.com/v1_1/your_cloud_name/image/upload', {
//                                method: 'POST',
//                                body: formData,
//                            });
//                            const data = await res.json();
//
//                            const imageUrl = data.secure_url;
//                            editor.insertHtml('<img src="' + imageUrl + '" />');
//                        });
//                    };
//                    reader.readAsDataURL(file);
//                });
//
//                document.body.appendChild(input);
//                input.click();
//            }
//        });
//
//        editor.ui.addButton('ImageCropUpload', {
//            label: 'Upload Cropped Image',
//            command: 'openCropDialog',
//            toolbar: 'insert',
//            icon: '/static/icons/crop-upload-icon.png'
//        });
//    }
//});