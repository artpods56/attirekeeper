const button = document.getElementById("rmbg-button");

button.addEventListener("click", async () => {
  const clothesDropZone = document.getElementById("clothes-drop-zone");
  const selectedImages = clothesDropZone.querySelectorAll(
    ".img-container.selected"
  );

  const backgroundDropZone = document.getElementById("background-drop-zone");
  const selectedBackground = backgroundDropZone.querySelector(
    ".img-container.selected"
  );

  if (selectedImages.length === 0) {
    alert("No images selected");
    return;
  }

  if (
    selectedBackground === null ||
    selectedBackground.length === 0 ||
    selectedBackground.length > 1
  ) {
    alert("No background selected or too many backgrounds selected");
    return;
  }

  const backgroundBlob = await fetch(selectedBackground.src).then((r) =>
    r.blob()
  );

  let imageBlobs = []; // Array to store the blobs of the images with added background
  for (let img of selectedImages) {
    let formData = new FormData();
    const responseBlob = await fetch(img.src).then((r) => r.blob());
    formData.append("file", responseBlob, "image.jpg");

    console.log("Sending request to remove background");
    let response = await fetch("http://localhost:8000/remove-bg/", {
      method: "POST",
      body: formData,
    });
    const imageBlob = await response.blob();
    console.log("Received response from remove-bg");
    // Add new background
    formData = new FormData();
    formData.append("files", backgroundBlob, "background.jpg");
    formData.append("files", imageBlob, "foreground.jpg");
    console.log("Sending request to add background");
    response = await fetch("http://localhost:8000/add-background/", {
      method: "POST",
      headers: {
        Accept: "application/json",
      },
      body: formData,
    });
    console.log("Received response from add-background");
    const finalImageBlob = await response.blob();
    imageBlobs.push(finalImageBlob);
  }

  function updateThumbnails(galleryID) {
    const Gallery = document.getElementById(galleryID);
    let thumbnailsContainer = document.getElementById(Gallery + "-thumbnails");
    if (!thumbnailsContainer) {
      const grid = document.createElement("div");
      grid.id = Gallery + "-thumbnails";
      grid.style.display = "grid";
      grid.style.gridTemplateColumns = "repeat(6, 1fr)";
      grid.style.gridAutoRows = "1fr";
      grid.style.alignItems = "stretch";

      grid.style.gap = "20px";
      grid.style.justifyItems = "center";
      grid.style.alignItems = "center";
      Gallery.appendChild(grid);
      return grid;
    }

    return thumbnailsContainer;
  }

  for (let i = 0; i < imageBlobs.length; i++) {

    galleryContainer = updateThumbnails("gallery");

    const imgContainer = document.createElement("div");
    imgContainer.style.position = "relative";
    imgContainer.style.display = "inline-block";
    imgContainer.classList.add("grid-item");


    const img = document.createElement("img");
    img.src = URL.createObjectURL(imageBlobs[i]);
    img.classList.add("img-container");
    img.style.width = "100%";
    img.style.height = "auto";
    img.style.borderRadius = "4px";

    imgContainer.appendChild(img);
    galleryContainer.appendChild(imgContainer);


  }
});
