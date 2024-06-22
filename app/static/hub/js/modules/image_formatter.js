function imageFormatter(value, row) {
    if (value && value.length > 0 && value[0].url) {
        return '<img src="' + value[0].url + '" style="max-width: 100px; max-height: 100px;">';
    }
    return '';
}