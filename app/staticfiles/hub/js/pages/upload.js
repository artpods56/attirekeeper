function setSelectorListener() {
    console.log("category changed");
    var category = document.getElementById("id_category").value;
    var topGarmentFields = document.getElementById("top-garments");
    var bottomGarmentFields = document.getElementById("bottom-garments");
  
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


  document.getElementById('uploadImage').addEventListener('change', function(event) {
    console.log("uploadImage");
    const files = event.target.files;
    const gallery = document.getElementById('gallery');

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();

        reader.onload = function(e) {
            const col = document.createElement('div');
            col.className = 'col';
            const card = `
                <div class="card shadow-sm">
                    <img class="bd-placeholder-img card-img-top" src="${e.target.result}" alt="Thumbnail">
                    <div class="card-body">
                        <p class="card-text">Newly uploaded image.</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="btn-group">
                                <button type="button" class="btn btn-sm btn-outline-secondary">Delete</button>
                                <button type="button" class="btn btn-sm btn-outline-secondary">Remove Background</button>
                            </div>
                            <small class="text-muted">Just now</small>
                        </div>
                    </div>
                </div>`;
            col.innerHTML = card;
            gallery.appendChild(col);
        };

        reader.readAsDataURL(file);
    }
});