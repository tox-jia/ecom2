console.log("imagecropupload plugin loaded");

CKEDITOR.plugins.add('imagecropupload', {
    icons: 'imagecropupload',
    init: function (editor) {
        editor.addCommand('openCropDialog', {
            exec: function () {
                // You can open a file input and attach Cropper.js logic here
                alert("Image crop dialog would open here.");
            }
        });
        editor.ui.addButton('ImageCropUpload', {
            label: 'Upload Cropped Image',
            command: 'openCropDialog',
            toolbar: 'insert',
            icon: '/static/icons/crop-upload-icon.png'
        });
    }
});