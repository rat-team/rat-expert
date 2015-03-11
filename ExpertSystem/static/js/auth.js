$(function(){
    addRegFormHandler();
    addLoginFormHandler();
});

function addLoginFormHandler() {
    $('#login-form').on('submit', function(event) {
        event.preventDefault();
        var serializedData = $(this).serialize();
        var error_span = $("#auth-error");

        $.post('/login/', serializedData)
            .done(function(data) {
                if(data.status == 'OK') {
                    window.location.replace("/")
                }
                else {
                    error_span.html(data.error);
                    error_span.show();
                }
            })
            .fail(function(data){
                error_span.html(data.error);
                error_span.show();
            });
    });
}

function addRegFormHandler() {
    $('#reg-form').on('submit', function(event) {
        event.preventDefault();
        var serializedData = $(this).serialize();
        var error_span = $("#auth-error");

        $.post('/registration/', serializedData)
            .done(function(data) {
                if(data.status == 'OK') {
                    window.location.replace("/")
                }
                else {
                    error_span.html(data.error);
                    error_span.show();
                }
            })
            .fail(function(data){
                error_span.html(data.error);
                error_span.show();
            });
    });
}
