function handleFileSelect() {
    var fileInput = document.getElementById('photoInput');
    var selectedFile = fileInput.files[0];
    var selectedFileNameElement = document.getElementById('selectedFileName');
    var selectedImageElement = document.getElementById('selectedImage');

    if (selectedFile) {


        // Display the selected image
        selectedImageElement.src = URL.createObjectURL(selectedFile);
        selectedImageElement.style.display = 'inline';

        // Send the selected file to Flask route
        var formData = new FormData();
        formData.append('file', 'aaa');
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/reset', true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log('Memory reset successfully');
                // Proceed with file upload after memory reset
                var formData1 = new FormData();
                // Append file data to formData
                formData1.append('file', selectedFile );
                var uploadXhr = new XMLHttpRequest();
                uploadXhr.open('POST', '/', true);
                uploadXhr.onload = function() {
                    if (uploadXhr.status === 200) {
                        console.log('File uploaded successfully');
                        window.location.reload();
                        // Handle response from the Flask route
                    } else {
                        console.error('Error uploading file');
                        // Handle error
                    }
                };
                uploadXhr.send(formData1);
            } else {
                console.error('Error resetting memory');
                // Handle error
            }
        };
        xhr.send(formData);

    } else {
        // If no file is selected, display a default message and hide the image
        selectedFileNameElement.textContent = 'Selected File: None';
        selectedImageElement.src = '';
        selectedImageElement.style.display = 'none';
    }

}
//Submit form
function submitForm() {
    // Disable the button
var button = document.getElementById('submitButton');
button.disabled = true;
    //Show hourglass
var hourglass=document.getElementById('hourglass')
hourglass.style.display='block'

var formData = new FormData();
formData.append('text', 'aaaa');
var xhr = new XMLHttpRequest();
xhr.open('POST', '/predict', true);
xhr.onload = function() {
    if (xhr.status === 200) {
        console.log('Prediction request sent successfully');
        button.disabled = false;
        window.location.reload();
        // Handle response from the server
    } else {
        console.error('Error sending prediction request');
        button.disabled = false;
        // Handle error
    }
};
xhr.send(formData);

}

// Show/Hide OUr story
function toggleStory() {
    var storySection = document.getElementById('showStory');
    storySection.classList.toggle('show-story');

    // Check if the toggle is on
    if (storySection.classList.contains('show-story')) {
        // Perform an AJAX request to fetch the story.html content
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/static/contents/our_story.html', true); // path to the story

        xhr.onload = function () {
            if (xhr.status === 200) {
                // Insert the fetched content into the story container
                document.getElementById('showStory').innerHTML = xhr.responseText;
            } else {
                console.error('Failed to fetch story.html');
            }
        };

        xhr.onerror = function () {
            console.error('Failed to fetch story.html');
        };

        xhr.send();
    } else {
        // Toggle is off, remove the story content from the container
        document.getElementById('showStory').innerHTML = '';
    }
}