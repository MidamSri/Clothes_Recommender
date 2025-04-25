document.getElementById('openGallery').addEventListener('click', () => {
    // Open the file picker for the gallery
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();

    input.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                document.getElementById('previewImage').src = e.target.result;
                document.getElementById('imageDetails').style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
});

document.getElementById('takePic').addEventListener('click', () => {
    // Open the camera
    const video = document.createElement('video');
    const popup = document.querySelector('.popup');
    popup.innerHTML = ''; // Clear the popup content

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            video.play();
            popup.appendChild(video);

            // Add a button to capture the photo
            const captureButton = document.createElement('button');
            captureButton.textContent = 'Capture';
            captureButton.style.marginTop = '10px';
            popup.appendChild(captureButton);

            captureButton.addEventListener('click', () => {
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, canvas.width, canvas.height);

                // Stop the video stream
                stream.getTracks().forEach((track) => track.stop());

                // Replace the video with the captured image
                popup.innerHTML = `
                    <img id="previewImage" src="${canvas.toDataURL('image/png')}" alt="Captured Image" style="width: 100%; margin-bottom: 10px;">
                    <select id="categorySelect">
                        <option value="" disabled selected>Select Category</option>
                        <option value="tops">Tops</option>
                        <option value="bottoms">Bottoms</option>
                        <option value="dresses">Dresses</option>
                        <option value="outfits">Outfits</option>
                    </select>
                    <input type="text" id="itemDescription" placeholder="Enter description" style="margin-top: 10px; width: 100%; padding: 10px;">
                    <button id="saveItem" style="margin-top: 10px; padding: 10px; width: 100%; background-color: #242C63; color: #FDFFEB; border: none; border-radius: 5px;">Save Item</button>
                `;

                // Add functionality to save the item
                document.getElementById('saveItem').addEventListener('click', () => {
                    const category = document.getElementById('categorySelect').value;
                    const description = document.getElementById('itemDescription').value;
                    const imageSrc = document.getElementById('previewImage').src;

                    if (!category || !description) {
                        alert('Please select a category and enter a description.');
                        return;
                    }

                    // Save the item to localStorage
                    const savedItems = JSON.parse(localStorage.getItem('closetItems')) || {};
                    if (!savedItems[category]) {
                        savedItems[category] = [];
                    }
                    savedItems[category].push({ src: imageSrc, name: description, heart: 'images/unfillheart.svg' });
                    localStorage.setItem('closetItems', JSON.stringify(savedItems));

                    alert('Item saved successfully!');
                    window.location.href = 'mycloset.html'; // Redirect back to the closet page
                });
            });
        })
        .catch((error) => {
            alert('Unable to access the camera');
            console.error(error);
        });
});

document.getElementById('saveItem').addEventListener('click', () => {
    const category = document.getElementById('categorySelect').value;
    const description = document.getElementById('itemDescription').value;
    const imageSrc = document.getElementById('previewImage').src;

    if (!category || !description) {
        alert('Please select a category and enter a description.');
        return;
    }

    // Save the item to localStorage
    const savedItems = JSON.parse(localStorage.getItem('closetItems')) || {};
    if (!savedItems[category]) {
        savedItems[category] = [];
    }
    savedItems[category].push({ src: imageSrc, name: description, heart: 'images/unfillheart.svg' });
    localStorage.setItem('closetItems', JSON.stringify(savedItems));

    alert('Item saved successfully!');
    window.location.href = 'mycloset.html'; // Redirect back to the closet page
});