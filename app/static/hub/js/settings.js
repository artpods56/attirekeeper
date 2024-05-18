function createOption(selectElement, value, text) {
  const option = document.createElement("option");
  option.value = value;
  option.text = text || value;
  return option;
}

function updateSelector(modelName) {
  fetch("/api/" + modelName + "/fields")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      var select = document.getElementById("fields");

      for (var i = 0; i < data.length; i++) {
        console.log("creating option for " + data[i]);
        select.appendChild(createOption(data[i], data[i]));
      }
    })
    .catch((error) => {
      console.error("Failed to fetch data:", error);
    });
}

updateSelector("measurements");
updateSelector("listing");

document
  .getElementById("id_description")
  .addEventListener("input", function () {
    var newDescription = document.getElementById("id_description").value;
    updatePreview(newDescription);
  });

document.getElementById("markup-button").addEventListener("click", function () {
  console.log("markup button clicked");
  var selectedValue = document.getElementById("fields").value;
  var descriptionInput = document.getElementById("id_description");
  const cursorPos = descriptionInput.selectionStart;
  const textBefore = descriptionInput.value.substring(0, cursorPos);
  const textAfter = descriptionInput.value.substring(
    cursorPos,
    descriptionInput.value.length
  );
  newDescription = textBefore + "{" + selectedValue + "}" + textAfter;

  descriptionInput.value = newDescription;
  // assuming the id of your description input field is 'description'

  updatePreview(newDescription);
});

function updatePreview(newDescription) {
  document.getElementById("preview").value = newDescription;
}

document
  .getElementById("template-selector")
  .addEventListener("change", function () {
    var selectedValue = document.getElementById("template-selector").value;
    if (selectedValue == "new") {
      document.getElementById("id_name").value = "";
      document.getElementById("id_description").value = "";
      return;
    }
    fetch("/api/template/" + selectedValue)
      .then((response) => response.json())
      .then((data) => {
        template_name = data["name"];
        template_description = data["description"];
        document.getElementById("id_name").value = template_name;
        document.getElementById("id_description").value = template_description;
        updatePreview(data);
      });
  });

function setFormAction() {
  var templateNameInput = document.getElementById("id_name");
  var selector = document.getElementById("template-selector");
  var selectedValue = selector.value;
  if (selectedValue === "new") {
    document.querySelector("form").reset();
    templateNameInput.disabled = false;
  } else {
    templateNameInput.disabled = true;
  }
  var action =
    selectedValue === "new" ? "/api/template/create/" : "/api/template/edit/";
  document.querySelector("form").action = action;
}

function toggleForm() {
  document
    .getElementById("template-selector")
    .addEventListener("change", setFormAction);
  setFormAction();
}

toggleForm();

