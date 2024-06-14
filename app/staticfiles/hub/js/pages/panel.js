window.addEventListener("load", () => {
  const widgets = document.querySelectorAll(".widget");
  widgets.forEach((widget) => {
    const width = getComputedStyle(widget).width;
    console.log(width);
    widget.style.minWidth = width;
  });
});

function createFileInput() {
  const fileInput = document.createElement("input");
  fileInput.setAttribute("type", "file");
  fileInput.setAttribute("multiple", "");
  fileInput.style.display = "none";
  return fileInput;
}

function createAddButton(addButtonID) {
  const addButton = document.createElement("button");
  addButton.classList.add("file-input");
  addButton.id = addButtonID;
  addButton.innerHTML = `+`;
  addButton.addEventListener("click", () => fileInput.click());

  return addButton;
}

const clothesDropZone = document.getElementById("clothes-drop-zone");
const clothesButton = document.getElementById("clothes-file-input");

const backgroundDropZone = document.getElementById("background-drop-zone");
const backgroundButton = document.getElementById("background-file-input");

function setupDropZone(dropZone) {
  const fileInput = createFileInput(); // Create a new instance for each drop zone
  dropZone.appendChild(fileInput);

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drop-zone--over");
  });

  dropZone.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drop-zone--over");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drop-zone--over");
    const files = e.dataTransfer.files;
    const dropZoneID = dropZone.id; // Local scope
    const buttonID = document.querySelector(`#${dropZoneID} button`).id;

    handleFiles(files, dropZoneID, buttonID);
    fileInput.value = "";
  });
}

function setupButtonInput(buttonInput, dropZoneID = null) {
  const fileInput = createFileInput(); // Create a new instance for each button
  buttonInput.appendChild(fileInput);

  buttonInput.addEventListener("click", () => {
    // const dropZoneID = buttonInput.parentNode.id; // Local scope
    fileInput.click();
  });

  fileInput.addEventListener("change", (e) => {
    const files = e.target.files;
    if (dropZoneID === null) {
      dropZoneID = buttonInput.parentNode.id; // Local scope
    }
    //const dropZoneID = buttonInput.parentNode.id; // Local scope
    const buttonID = buttonInput.id;
    handleFiles(files, dropZoneID, buttonID);
    fileInput.value = "";
  });
}

setupDropZone(backgroundDropZone);
setupButtonInput(backgroundButton);

setupDropZone(clothesDropZone);
setupButtonInput(clothesButton);

function updateThumbnails(dropZoneID) {
  const dropZone = document.getElementById(dropZoneID);
  let thumbnailsContainer = document.getElementById(dropZoneID + "-thumbnails");
  if (!thumbnailsContainer) {
    const grid = document.createElement("div");
    grid.id = dropZoneID + "-thumbnails";
    grid.style.display = "grid";
    grid.style.gridTemplateColumns = "repeat(4, 1fr)";
    grid.style.gridAutoRows = "1fr";
    grid.style.alignItems = "stretch";

    grid.style.gap = "20px";
    grid.style.justifyItems = "center";
    grid.style.alignItems = "center";
    dropZone.appendChild(grid);
    return grid;
  }

  return thumbnailsContainer;
}

function createThumbnail(file, dropZoneID, buttonID, maxImages) {
  const buttonInput = document.getElementById(buttonID);

  const reader = new FileReader();

  reader.onload = function (e) {
    thumbnailsContainer = document.getElementById(dropZoneID);
    let imageCounter =
      thumbnailsContainer.querySelectorAll(".img-container").length;
    imageCounter++;
    if (imageCounter > maxImages) {
      return;
    }
    console.log("debugging");
    console.log("imageCounter: ", imageCounter);
    const imgContainer = document.createElement("div");
    imgContainer.style.position = "relative";
    imgContainer.style.display = "inline-block";
    imgContainer.classList.add("grid-item");

    const img = document.createElement("img");
    img.classList.add("img-container");
    img.src = e.target.result;
    img.style.width = "100%";
    img.style.height = "auto";
    img.style.borderRadius = "4px";

    const removeBtn = document.createElement("button");
    removeBtn.classList.add("img-remove-button");

    removeBtn.onclick = function (dropZoneID) {
      imgContainer.remove();
      // let thumbnailsContainer = document.getElementById(dropZoneID);
      let numberOfPhotos =
        thumbnailsContainer.querySelectorAll(".img-container").length;
      // if addButton is hidden and number of photos is less than maxImages, show addButton
      if (numberOfPhotos < maxImages && addButton.hidden) {
        addButton.hidden = false;
      }

      imgContainers = thumbnailsContainer.querySelector(".img-container");

      if (!imgContainers) {
        console.log("No longer contains imgContainer");
        addButton.remove();
        buttonInput.hidden = false;
      }
    };

    thumbnailsContainer = updateThumbnails(dropZoneID);

    addButton = document.getElementById(buttonID);

    const elementsToRemove =
      thumbnailsContainer.querySelectorAll(".file-input");
    elementsToRemove.forEach((element) => element.remove());

    addButton = createAddButton(buttonID);
    setupButtonInput(addButton, dropZoneID);

    imgContainer.appendChild(img);
    imgContainer.appendChild(removeBtn);

    imgContainer.addEventListener("click", () => {
      console.log("clicked");
      img.classList.toggle("selected");
    });

    thumbnailsContainer.appendChild(imgContainer);

    thumbnailsContainer.appendChild(addButton);
    let numberOfPhotos =
      thumbnailsContainer.querySelectorAll(".img-container").length;

    if (numberOfPhotos >= maxImages) {
      addButton.hidden = true;
    }

    if (numberOfPhotos >= 1) {
      buttonInput.hidden = true;
    }
  };
  reader.readAsDataURL(file);
}

function handleFiles(files, dropZoneID, buttonID) {
  if (dropZoneID === "clothes-drop-zone") {
    maxImages = 20;
  } else if (dropZoneID === "background-drop-zone") {
    maxImages = 4;
  }
  for (let i = 0; i < files.length; i++) {
    createThumbnail(files[i], dropZoneID, buttonID, maxImages);
  }
}

function setSelectorListener() {
  console.log("category changed");
  var category = document.getElementById("id_category").value;
  var topGarmentFields = document.getElementById("top-garment-fields");
  var bottomGarmentFields = document.getElementById("bottom-garment-fields");

  // Ukryj wszystkie pola
  topGarmentFields.style.display = "none";
  bottomGarmentFields.style.display = "none";

  // topGarmentFields.style.display = 'block';
  // Wyświetl odpowiednie pola w zależności od wybranej kategorii
  if (category === "top_garment") {
    topGarmentFields.style.display = "block";
  } else if (category === "bottom_garment") {
    bottomGarmentFields.style.display = "block";
  } else {
    return;
  }
}

function toggleForm() {
  document
    .getElementById("id_category")
    .addEventListener("change", setSelectorListener);
  setSelectorListener();
}

toggleForm();

function populateInput() {
  const selectedImages = document.querySelectorAll(
    ".img-container.selected img"
  );
  const imageData = Array.from(selectedImages).map((img) => img.src); // Get src if it's a data URL
  document.getElementById("id_image").value = JSON.stringify(imageData);
  console.log("imageData: ", imageData);
}

