console.log("panel2.js loaded");

import { isValidImage } from "../modules/is_valid_image.js";

// Function to convert multiple image URLs to blobs
async function urlsToBlobs(images) {
  console.log("images", images);
  const responses = await Promise.all(
    images.map((image) => {
      const response = fetch(image.url);
      // check response
      return response;
    })
  );

  // transform responses to blobs
  const blobs = await Promise.all(responses.map((response) => response.blob()));

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
  reader.onload = function (e) {
    const col = document.createElement("div");
    col.className = "col";
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

    const cardElement = document.createElement("div");
    cardElement.innerHTML = card;

    const removeButton = cardElement.querySelector(".rm-card-btn");
    removeButton.addEventListener("click", function () {
      col.remove();
    });

    const removeBgButton = cardElement.querySelector(".rm-bg-btn");

    removeBgButton.addEventListener("click", async function () {
      const bgImageInput = document.getElementById("upload-bg-image");
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
      let add_bg_response = await fetch(
        "http://localhost:8000/add-background/",
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
          body: formData,
        }
      );

      const finalImageBlob = await add_bg_response.blob();

      const cardImg = cardElement.querySelector(".item-image");
      cardImg.src = URL.createObjectURL(finalImageBlob);
    });

    col.appendChild(cardElement);
    gallery.appendChild(col);
  };

  reader.readAsDataURL(file);
}

document
  .getElementById("id_image")
  .addEventListener("change", function (event) {
    const files = Array.from(event.target.files);
    const gallery = document.getElementById("gallery");

    files.forEach(async (file) => createItemCards(file));
  });

document
  .getElementById("template-selector")
  .addEventListener("change", function () {
    updatePreviewText();
  });

function updatePreviewText() {
  const descriptionValue = document.getElementById("template-selector").value;
  const previewText = document.getElementById("preview-text");
  const itemData = JSON.parse(document.getElementById("item-data").textContent);
  let replacedText = descriptionValue;
  for (const [key, value] of Object.entries(itemData)) {
    if (value) {
      console.log(`Key: ${key}, Value: ${value}`);
      const marker = `{${key}}`;
      replacedText = replacedText.replace(marker, value);
      console.log(`Replacing ${marker} with ${value}`);
    } else {
      console.log(`Key: ${key}, Value: ${value}`);
      const marker = `{${key}}`;
      replacedText = replacedText.replace(marker, "-");
      console.log(`Replacing ${marker} with '-'`);
    }
  }
  previewText.value = replacedText;
}

async function runOnStart() {
  // Run your code here
  updatePreviewText();
  console.log("runOnStart");
  const photosData = JSON.parse(
    document.getElementById("photos-data").textContent
  );

  // get array of image blobs by passing ulrs from json stored as photosData
  // wait for all images to be fetched and converted to blobs
  const imagesBlobsPromises = photosData.map((photo) =>
    fetch(photo.url).then((response) => response.blob())
  );

  // Wait for all promises to resolve
  const imagesBlobs = await Promise.all(imagesBlobsPromises);

  console.log("imagesBlobs", imagesBlobs);
  imagesBlobs.forEach(async (file) => createItemCards(file));
}

function setSelectorListener() {
  console.log("category changed m");
  var category = document.getElementById("id_category").value;
  var topGarmentFields = document.getElementById("top-garment-measurements");
  var bottomGarmentFields = document.getElementById(
    "bottom-garment-measurements"
  );

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
      sizeSelectorOptions[i].style.display = "block";
    } else {
      sizeSelectorOptions[i].style.display = "none";
    }
  }
  sizeSelector.disabled = false;
}

function toggleForm() {
  document
    .getElementById("id_category")
    .addEventListener("change", setSelectorListener);
  setSelectorListener();
}

toggleForm();

document
  .getElementById("id-listing-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const formProps = Object.fromEntries(formData);

    for (const [key, value] of Object.entries(formProps)) {
      console.log(`${key}: ${value}`);
    }

    // Collect selected files from containers
    const selectedImages = document.querySelectorAll(".item-image");

    // Clear the existing files input
    formData.delete("image");

    selectedImages.forEach(async (imgElement, index) => {
      const src = imgElement.src;
      if (src.startsWith("data:image")) {
        const imageBlob = await fetch(src).then((r) => r.blob());
      }
    });

    // Wait for all images to be appended before sending the form
    Promise.all(
      Array.from(selectedImages).map(async (imgElement, index) => {
        const src = imgElement.src;
        if (src.startsWith("data:image")) {
          const imageBlob = await fetch(src).then((r) => r.blob());
          formData.append("image", imageBlob, `image${index}.png`);
        }
      })
    ).then(() => {
      $.ajax({
        url: event.target.action,
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function (xhr) {
          xhr.setRequestHeader(
            "X-CSRFToken",
            document.querySelector("[name=csrfmiddlewaretoken]").value
          );
        },
        success: function (response) {
          console.log("Files uploaded successfully");
        },
        error: function (error) {
          console.log("An error occurred while uploading files");
        },
      });
    });
  });

document
  .getElementById("listing-selector")
  .addEventListener("change", function () {
    const url = `http://192.168.1.12:8001/items/view/${this.value}/`;
    window.location.href = url;
  });

if (document.readyState !== "loading") {
  runOnStart();
} else {
  document.addEventListener("DOMContentLoaded", function () {
    runOnStart();
  });
}
