export function isValidImage(inputFile) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        
        reader.onload = function() {
            var image = new Image();
            
            image.onload = function() {
                if ('naturalHeight' in this) {
                    if (this.naturalHeight + this.naturalWidth === 0) {
                        this.onerror();
                        resolve(false);
                        return;
                    }
                } else if (this.width + this.height == 0) {
                    this.onerror();
                    resolve(false);
                    return;
                }
                resolve(true);
            };
            
            image.onerror = function() {
                resolve(false);
            };
            
            image.src = reader.result;
        };
        
        reader.readAsDataURL(inputFile);
    });
}