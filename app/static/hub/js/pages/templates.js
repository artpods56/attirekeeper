// Function to load listing data
async function loadListingData() {
    const listingId = document.getElementById('listing-selector').value;
    const url = `http://localhost:8001/api/listings/${listingId}/`;

    console.log(url);
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to update preview text
function updatePreviewText() {
    const descriptionValue = document.getElementById('id_description').value;
    const previewText = document.getElementById('preview-text');

    Promise.all([listingData]).then(function(values) {
        console.log('Updating preview text with listing data');
        data = values[0].rows[0];
        const skipFields = ['photos'];
        let replacedText = descriptionValue;
        for (const [key, value] of Object.entries(data)) {
            if (value && !skipFields.includes(key)) {
                console.log(`Key: ${key}, Value: ${value}`);
                const marker = `{${key}}`;
                replacedText = replacedText.replace(marker, value);
                console.log(`Replacing ${marker} with ${value}`);
            }
        }
        previewText.value = replacedText;
    });
}

// Global variable to store listing data
let listingData = loadListingData();

// Event listeners
window.addEventListener('DOMContentLoaded', updatePreviewText);

document.getElementById('listing-selector').addEventListener('change', async function() {
    listingData = await loadListingData();
    updatePreviewText();
});

document.getElementById('insert-button').addEventListener('click', function() {
    const selectedField = document.getElementById('field-selector').value;
    const descriptionField = document.getElementById('id_description');
    const cursorPosition = descriptionField.selectionStart;
    const insertedValue = `{${selectedField}}`;

    descriptionField.value = 
        descriptionField.value.slice(0, cursorPosition) + 
        insertedValue + 
        descriptionField.value.slice(cursorPosition);

    updatePreviewText();
});

document.getElementById('id_description').addEventListener('input', updatePreviewText);

document.getElementById('template-selector').addEventListener('change', function() {
    const url = `http://localhost:8001/templates/view/${this.value}/`;
    window.location.href = url;
});