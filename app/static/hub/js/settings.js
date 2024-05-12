
function createOption(value, text) {
    var option = document.createElement('option');
    option.value = value;
    option.text = text;
    return option;
}


document.getElementById('id_category').addEventListener('change', function() {
    console.log('changed');
    var category = this.value;
    console.log(category);
    fetch('/get_fields/' + category + '/')
        .then(response => response.json())
        .then(data => {
            var select = document.getElementById('fields');
            select.innerHTML = '';
            select.appendChild(createOption(null, 'Select a field...'));
            select.appendChild(createOption('title', 'title'));
            select.appendChild(createOption('description', 'description'));
            select.appendChild(createOption('size', 'size'));
            for (var i = 0; i < data.length; i++) {
                var option = document.createElement('option');
                option.value = data[i];
                option.text = data[i];
                select.appendChild(option);
            }
        });
});






document.getElementById('id_description').addEventListener('input', function() {
    var newDescription = document.getElementById('id_description').value;
    updatePreview(newDescription);
});


document.getElementById('markup-button').addEventListener('click', function() {

    console.log('markup button clicked');
    var selectedValue = document.getElementById('fields').value;
    var descriptionInput = document.getElementById('id_description');
    const cursorPos = descriptionInput.selectionStart;
    const textBefore = descriptionInput.value.substring(0, cursorPos);
    const textAfter = descriptionInput.value.substring(cursorPos, descriptionInput.value.length);
    newDescription = textBefore + '{' + selectedValue + '}' + textAfter;

    descriptionInput.value = newDescription;
    // assuming the id of your description input field is 'description'

    updatePreview(newDescription);
  });
  
  function updatePreview(newDescription) {
    document.getElementById('preview').value = newDescription;
}
