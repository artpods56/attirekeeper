const fileInput = document.createElement("input");

fileInput.setAttribute("type", "file");
fileInput.setAttribute("multiple", "");
fileInput.style.display = "none";

const dropZone = document.getElementById("drop-zone");
const buttonInput = document.getElementById("file-input");

dropZone.appendChild(fileInput);
buttonInput.appendChild(fileInput);

const addButton = document.createElement("div");
addButton.classList.add("file-input");
addButton.innerHTML = '<button id="file-input">+</button>';
addButton.addEventListener("click", () => fileInput.click());
addButton.style.cursor = "pointer";
addButton.style.display = "inline-block";
addButton.style.width = "50px";
addButton.style.height = "50px";
addButton.style.display = "flex";
addButton.style.fontSize = "30px";
addButton.style.color = "#ccc";

buttonInput.addEventListener("click", () => fileInput.click());

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
  handleFiles(files);
});

fileInput.addEventListener("change", (e) => {
  const files = e.target.files;
  handleFiles(files);
});

function updateThumbnails() {
  const thumbnailsContainer = document.getElementById("thumbnails");
  if (!thumbnailsContainer) {
    const grid = document.createElement("div");
    grid.id = "thumbnails";
    grid.style.display = "grid";
    grid.style.gridTemplateColumns = "repeat(5, 1fr)";
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

function createThumbnail(file) {
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
      const thumbnailsContainer = updateThumbnails();
      imgContainers = thumbnailsContainer.querySelector(".img-container");

      if (!imgContainers) {
        console.log("No longer contains imgContainer");
        addButton.remove();
        buttonInput.hidden = false;
      }
    };

    imgContainer.appendChild(img);
    imgContainer.appendChild(removeBtn);

    imgContainer.addEventListener("click", () => {
      console.log("clicked");
      img.classList.toggle("selected");
    });
    imgContainer.appendChild(addButton);

    const thumbnailsContainer = updateThumbnails();

    if (thumbnailsContainer.contains(addButton)) {
      thumbnailsContainer.removeChild(addButton);
    }

    thumbnailsContainer.appendChild(imgContainer);

    if (thumbnailsContainer.children.length < 20) {
      thumbnailsContainer.appendChild(addButton);
    }

    if (thumbnailsContainer.children.length >= 1) {
      buttonInput.hidden = true;
    }
  };
  reader.readAsDataURL(file);
}

function handleFiles(files) {
  for (let i = 0; i < files.length; i++) {
    createThumbnail(files[i]);
  }

  fileInput.value = "";
}

const rmbgButton = document.getElementById("rmbg-button");

const bgButton = document.getElementById("bg-select-button");

rmbgButton.addEventListener('click', async () => {
    console.log('rmbgButton clicked');
    const selectedImages = document.querySelectorAll('img.img-container.selected');
    
    if (selectedImages.length === 0) {
        alert('No images selected');
        return;
    }
    for (let img of selectedImages) {
        let formData = new FormData();
        const responseBlob = await fetch(img.src).then(r => r.blob()); 
        formData.append('file', responseBlob, 'image.jpg');
  
        const response = await fetch('http://localhost:8000/remove-bg/', {
            method: 'POST',
            body: formData,
        });
        const imageBlob = await response.blob();
        const imageUrl = URL.createObjectURL(imageBlob);
        createThumbnail(imageBlob);
    }
  });