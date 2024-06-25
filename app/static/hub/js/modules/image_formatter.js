function imageFormatter(value, row) {
    if (value && value.length > 0 && value[0].url) {
        return '<img class="img-thumbnail" src="' + value[0].url + '" style="object-fit: cover; width: 100px; height: 100px;">';
    }
    else {
        let container = document.createElement('div');
        container.className = 'img-thumbnail';
        container.style.cssText = 'padding: 25px; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; object-fit: cover;';
        
        // Create the Bootstrap icon element
        let icon = document.createElement('i');
        icon.className = 'bi bi-images text-secondary';
        icon.style.fontSize = '32px';
        
        // Append the icon to the container
        container.appendChild(icon);
        return container.outerHTML;
    }
}


