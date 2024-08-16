console.log("panel2.js loaded");

import { isValidImage } from '../modules/is_valid_image.js';

// Function to convert multiple image URLs to blobs
async function urlsToBlobs(images) {
    console.log("images", images);
    const responses = await Promise.all(images.map(image => {
        const response = fetch(image.url);
        // check response
        return response
    }));

    // transform responses to blobs
    const blobs = await Promise.all(responses.map(response => response.blob()));

    console.log("blobs", blobs);
    return blobs;
}

async function createItemCards(file) {
    const isValid = await isValidImage(file);
    if (!isValid) {
        console.log(`File ${file.name} is not a valid image. Skipping.`);
        return;
    }

const reader = new FileReader();
reader.onload = function(e) {
const col = document.createElement('div');
col.className = 'col';
const card = `
    <div class="card shadow-sm">
        <img class="item-image" src="${e.target.result}" alt="Thumbnail">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
          
            <div class="btn-group" role="group">
            <button type="button" class="btn border-secondary  btn-sm btn-outline-secondary rm-card-btn">Remove</button>
            <button type="button" class="btn border-secondary  btn-outline-secondary border-start-0 dropdown-toggle dropdown-toggle-split" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false"></button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
              <li><a class="dropdown-item" href="#">Rotate left</a></li>
              <li><a class="dropdown-item" href="#">Rotate right</a></li>
              <li><a class="dropdown-item rm-bg-btn" href="#">Remove background</a></li>
              <li><a class="dropdown-item" href="#">Something else here</a></li>
            </ul>
          </div>
            </div>
        </div>
    </div>`;

const cardElement = document.createElement('div');
cardElement.innerHTML = card;

const removeButton = cardElement.querySelector('.rm-card-btn');
removeButton.addEventListener('click', function() {
    col.remove();
});

const removeBgButton = cardElement.querySelector('.rm-bg-btn');

removeBgButton.addEventListener('click', async function() {
    const bgImageInput = document.getElementById('upload-bg-image');
    const bgImageFile = bgImageInput.files[0];
    if (!bgImageFile) {
        console.log("No background image selected. Skipping.");
        return;
    }
    const bgIsValid = await isValidImage(bgImageFile);
    if (!bgIsValid) {
        console.log(`File ${bgImageFile.name} is not a valid image. Skipping.`);
        return;
    }

    let formData = new FormData();
    const responseBlob = new Blob([file], { type: file.type });
    formData.append("file", responseBlob, file.name);

    console.log("Sending request to remove background");
    let rm_bg_response = await fetch("http://localhost:8000/remove-bg/", {
    method: "POST",
    body: formData,
    });
    const imageBlob = await rm_bg_response.blob();

    console.log("bgImageFile", bgImageFile);
    const bgBlob = new Blob([bgImageFile], { type: bgImageFile.type });

    formData = new FormData();
    formData.append("files", bgBlob, "background.jpg");
    formData.append("files", imageBlob, "foreground.jpg");

    console.log("Sending request to add background");
    let add_bg_response = await fetch("http://localhost:8000/add-background/", {
      method: "POST",
      headers: {
        Accept: "application/json",
      },
      body: formData,
    });


    const finalImageBlob = await add_bg_response.blob();


    const cardImg = cardElement.querySelector('.item-image');
    cardImg.src = URL.createObjectURL(finalImageBlob);


});

col.appendChild(cardElement);
gallery.appendChild(col);
};


reader.readAsDataURL(file);
}


document.getElementById('id_image').addEventListener('change', function(event) {
    const files = Array.from(event.target.files);
    const gallery = document.getElementById('gallery');


    files.forEach(async (file) => createItemCards(file));
});

document.addEventListener('DOMContentLoaded', async  function() {
    const photosData = JSON.parse(document.getElementById('photos-data').textContent);

    // get array of image blobs by passing ulrs from json stored as photosData
    // wait for all images to be fetched and converted to blobs
    const imagesBlobsPromises = photosData.map(photo => 
        fetch(photo.url).then(response => response.blob())
    );

    // Wait for all promises to resolve
    const imagesBlobs = await Promise.all(imagesBlobsPromises);

    console.log("imagesBlobs", imagesBlobs);
    imagesBlobs.forEach(async (file) => createItemCards(file));
});
// document.getElementById('id_category').addEventListener('change', function() {
//     // Get the selected value from the first selector
//     console.log("category changed");
//     var selectedClass = this.value;

//     // Get all options from the second selector
//     var options = document.getElementById('id_size').options;
  
//     // Loop through all options in the second selector
//     for (var i = 0; i < options.length; i++) {
//       // If the option's class matches the selected value, show it, otherwise hide it

//       if (options[i].classList.contains(selectedClass)) {
//         options[i].style.display = 'block';
//       } else {
//         options[i].style.display = 'none';
//       }
//     }
//   });


function setSelectorListener() {
    console.log("category changed m");
    var category = document.getElementById("id_category").value;
    var topGarmentFields = document.getElementById("top-garment-measurements");
    var bottomGarmentFields = document.getElementById("bottom-garment-measurements");
  
    // Ukryj wszystkie pola
    topGarmentFields.style.display = "none";
    bottomGarmentFields.style.display = "none";
  
    var sizeSelector = document.getElementById("id_size");
    var sizeSelectorOptions = sizeSelector.options;
  
    sizeSelector.disabled = true;

    if (category === "top_garment") {
      topGarmentFields.style.display = "inline-table";
    } else if (category === "bottom_garment") {
      bottomGarmentFields.style.display = "inline-table";
    } else {
      sizeSelector.disabled = true;
      return;
    }
  



    

    for (var i = 0; i < sizeSelectorOptions.length; i++) {
        if (sizeSelectorOptions[i].classList.contains(category)) {
            sizeSelectorOptions[i].style.display = 'block';

        } else {
            sizeSelectorOptions[i].style.display = 'none';
        }
    }
    sizeSelector.disabled = false;

  }
  
  function toggleForm() {
    document.getElementById("id_category").addEventListener("change", setSelectorListener);
    setSelectorListener();
  }
  
  toggleForm();

  document.getElementById('id-listing-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const formProps = Object.fromEntries(formData);

    for (const [key, value] of Object.entries(formProps)) {
        console.log(`${key}: ${value}`);
    }

    // Collect selected files from containers
    const selectedImages = document.querySelectorAll('.item-image');
    
    // Clear the existing files input
    formData.delete('image');

    selectedImages.forEach(async (imgElement, index) => {
        const src = imgElement.src;
        if (src.startsWith('data:image')) {
            const imageBlob = await fetch(src).then(r => r.blob()); 
        }
    });

    // Wait for all images to be appended before sending the form
    Promise.all(Array.from(selectedImages).map(async (imgElement, index) => {
        const src = imgElement.src;
        if (src.startsWith('data:image')) {
            const imageBlob = await fetch(src).then(r => r.blob()); 
            formData.append('image', imageBlob, `image${index}.png`);
        }
    })).then(() => {
        $.ajax({
            url: event.target.action,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);
            },
            success: function(response) {
                console.log('Files uploaded successfully');
            },
            error: function(error) {
                console.log('An error occurred while uploading files');
            }
        });
    });
});



document.getElementById("copyImagesButton").addEventListener("click", async () => {
    try {
        // Get all image elements on the page
        const images = document.querySelectorAll(".item-image");

        // Create an array to store ClipboardItem objects
        const clipboardItems = [];

        for (let img of images) {
            // Fetch the image data as a blob
            const response = await fetch(img.src);
            const blob = await response.blob();

            // Create a ClipboardItem with the blob
            const clipboardItem = new ClipboardItem({ [blob.type]: blob });

            // Add it to the clipboardItems array
            clipboardItems.push(clipboardItem);
        }

        // Use the Clipboard API to write the images to the clipboard
        await navigator.clipboard.write(clipboardItems);

        alert("Images copied to clipboard. You can now paste them elsewhere.");
    } catch (error) {
        console.error("Failed to copy images: ", error);
        alert("Failed to copy images. Please check console for details.");
    }
});