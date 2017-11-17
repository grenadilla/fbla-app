$(document).ready(function($) {
    $(".clickable-book").click(function() {
        window.location.href = $(this).data("href");
    });
});
