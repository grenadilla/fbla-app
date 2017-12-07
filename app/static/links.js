$(document).ready(function($) {
    $(".clickable-link").click(function() {
        window.location.href = $(this).data("href");
    });
    $(".cancel-button").click(function() {
        history.go(-1);
    });
});
