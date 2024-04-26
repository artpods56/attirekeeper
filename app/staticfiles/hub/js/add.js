const fileInput = document.createElement("input");
fileInput.setAttribute("type", "file");
fileInput.setAttribute("multiple", "");
fileInput.style.display = "none";


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


function setupDropZone(dropZone) {
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
    handleFiles(files);
  });
}

function setupButtonInput(buttonInput) {
  buttonInput.appendChild(fileInput);

  buttonInput.addEventListener("click", () => fileInput.click());

  buttonInput.addEventListener("change", (e) => {
    const files = e.target.files;
    handleFiles(files);
  });
}

const clothesDropZone = document.getElementById("clothes-drop-zone");
const clothesButton = document.getElementById("clothes-file-input");

const backgroundDropZone = document.getElementById("background-drop-zone");
const backgroundButton = document.getElementById("background-file-input");

setupDropZone(clothesDropZone);
setupButtonInput(clothesButton);

setupDropZone(backgroundDropZone);
setupButtonInput(backgroundButton);