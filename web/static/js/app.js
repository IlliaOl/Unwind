$(document).foundation()

// Docs: https://flatpickr.js.org/
$(function () {
    $('#datetime-input').flatpickr({
        altInput: true,
        altFormat: "F j, Y, H:i",
        enableTime: true,
        time_24hr: true,
        dateFormat: "Y-m-d H:i",
        "locale": "ru"
    });
});
