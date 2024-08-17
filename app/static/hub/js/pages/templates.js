// Function to load listing data

// Function to update preview text
function updatePreviewText() {
  const descriptionValue = document.getElementById("id_description").value;
  const previewText = document.getElementById("preview-text");
  const itemData = JSON.parse(
    document.getElementById("listing-selector").value.replace(/'/g, '"')
  );
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

// Event listeners
window.addEventListener("DOMContentLoaded", updatePreviewText);

document
  .getElementById("listing-selector")
  .addEventListener("change", async function () {
    updatePreviewText();
  });

document.getElementById("insert-button").addEventListener("click", function () {
  const selectedField = document.getElementById("field-selector").value;
  const descriptionField = document.getElementById("id_description");
  const cursorPosition = descriptionField.selectionStart;
  const insertedValue = `{${selectedField}}`;

  descriptionField.value =
    descriptionField.value.slice(0, cursorPosition) +
    insertedValue +
    descriptionField.value.slice(cursorPosition);

  updatePreviewText();
});

document
  .getElementById("id_description")
  .addEventListener("input", updatePreviewText);

document
  .getElementById("template-selector")
  .addEventListener("change", function () {
    const options = document.getElementById("template-selector").options;
    const selectedId = options[options.selectedIndex].id;
    const url = `http://192.168.1.12:8001/templates/view/${selectedId}/`;
    window.location.href = url;
  });

async function runOnStart() {
  updatePreviewText();
}

if (document.readyState !== "loading") {
  runOnStart();
} else {
  document.addEventListener("DOMContentLoaded", function () {
    runOnStart();
  });
}
