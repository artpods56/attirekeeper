
const dropZone = document.getElementById('drop_zone');
const fileInput = document.getElementById('file_input');
const imagesPreview = document.getElementById('images_preview');
const submitButton = document.getElementById('submit_btn');
const resultsPreview = document.getElementById('results_preview');

dropZone.addEventListener("dragover", (e) => {
  e.stopPropagation();
  e.preventDefault();
  e.dataTransfer.dropEffect = "copy";
});

dropZone.addEventListener("drop", (e) => {
  e.stopPropagation();
  e.preventDefault();
  const files = e.dataTransfer.files;
  handleFiles(files);
});

dropZone.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", () => {
  handleFiles(fileInput.files);
});

function handleFiles(files) {
  for (let i = 0; i < files.length; i++) {
    displayImage(files[i]);
  }
}

function displayImage(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const imageContainer = document.createElement('div');
        imageContainer.className = 'image-container';
        const img = document.createElement('img');
        img.src = e.target.result;

        imageContainer.appendChild(img);
        imagesPreview.appendChild(imageContainer);

        imageContainer.addEventListener('click', () => {
            imageContainer.classList.toggle('selected');
        });
    };
    reader.readAsDataURL(file);
}

submitButton.addEventListener('click', async () => {
  const selectedImages = document.querySelectorAll('.image-container.selected img');

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

      const resultContainer = document.createElement('div');
      resultContainer.className = 'image-container';

      const resultImg = document.createElement('img');
      resultImg.src = imageUrl;
      resultContainer.appendChild(resultImg);

      resultsPreview.appendChild(resultContainer);
  }
});

function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(
      " active",
      ""
    );
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}