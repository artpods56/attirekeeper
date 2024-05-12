// document.getElementById('template-input').addEventListener('input', updatePreview);

// function insertTag(tag) {
//     const textarea = document.getElementById('template-input');
//     const cursorPos = textarea.selectionStart;
//     const textBefore = textarea.value.substring(0, cursorPos);
//     const textAfter = textarea.value.substring(cursorPos, textarea.value.length);
//     textarea.value = textBefore + '{' + tag + '}' + textAfter;
//     updatePreview();
// }

// function updatePreview() {
//     const templateText = document.getElementById('template-input').value;
//     document.getElementById('preview').innerText = templateText;
// }