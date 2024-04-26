function createFileInput() {
  const fileInput = document.createElement("input");
  fileInput.setAttribute("type", "file");
  fileInput.setAttribute("multiple", "");
  fileInput.style.display = "none";
  return fileInput;
}

function createAddButton(addButtonID) {
  const addButton = document.createElement("div");
  addButton.classList.add("grid-button");
  addButton.id = addButtonID;
  addButton.innerHTML = `<button>+</button>`; 
  addButton.addEventListener("click", () => fileInput.click());
  addButton.style.cursor = "pointer";
  addButton.style.display = "inline-block";
  addButton.style.width = "50px";
  addButton.style.height = "50px";
  addButton.style.display = "flex";
  addButton.style.fontSize = "30px";
  addButton.style.color = "#ccc";
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
    grid.style.gridTemplateColumns = "repeat(6, 1fr)";
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

function createThumbnail(file, dropZoneID, buttonID) {
  const buttonInput = document.getElementById(buttonID);

  const reader = new FileReader();

  reader.onload = function (e) {
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
    removeBtn.innerText = "X";
    removeBtn.style.position = "absolute";
    removeBtn.style.top = "5px";
    removeBtn.style.right = "5px";
    removeBtn.style.border = "none";
    removeBtn.style.background = "white";
    removeBtn.style.color = "black";
    removeBtn.style.borderRadius = "30%";
    removeBtn.style.cursor = "pointer";

    removeBtn.onclick = function () {
      imgContainer.remove();
      const thumbnailsContainer = updateThumbnails(dropZoneID);
      imgContainers = thumbnailsContainer.querySelector(".img-container");

      if (!imgContainers) {
        console.log("No longer contains imgContainer");
        addButton.remove();
        buttonInput.hidden = false;
      }
    };

    const thumbnailsContainer = updateThumbnails(dropZoneID);

    addButton = document.getElementById(buttonID);

    const elementsToRemove = thumbnailsContainer.querySelectorAll('.grid-button');
    elementsToRemove.forEach(element => element.remove());

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

    if (thumbnailsContainer.children.length >= 1) {
      buttonInput.hidden = true;
    }
  };
  reader.readAsDataURL(file);
}

function handleFiles(files, dropZoneID, buttonID) {
  for (let i = 0; i < files.length; i++) {
    createThumbnail(files[i], dropZoneID, buttonID);
  }
}
