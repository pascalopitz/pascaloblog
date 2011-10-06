$(function() {
    $("select, input:checkbox, input:radio, input:file, input:text, textarea, button, a.button").uniform();

    window.setTimeout(function() {
        $('.message').fadeOut();
    }, 3000);

    $('body').delegate('.show-more', 'click', function(e) {
        var link = this;
        
        $.get($(link).attr('href'), function(data) {
            $(link).before(data);
            $(link).remove();
        });
        
        return false;
    });
});
