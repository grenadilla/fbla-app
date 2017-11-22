$(document).ready(function($) {
    $(".clickable-link").click(function() {
        window.location.href = $(this).data("href");
    });
});
