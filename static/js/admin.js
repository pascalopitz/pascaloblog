$(function() {
    //hide messages
    window.setTimeout(function() {
        $('.message').fadeOut();
    }, 3000);
    
    //initialize for styling
    $("select, input:checkbox, input:radio, input:file, input:text, textarea, button, a.button").filter(':not(.uniform)').addClass('uniform').uniform();
    
    //Type title updates url token
    if($('input#url_token').val() == '') {
        var update = function(e) {
            var title = $(this).val().replace(/[^1-9a-z]/gi, '-');
            $('input#url_token').val(title);
        };
        
        $('input#title').bind('keyup', update);
        $('input#url_token').focus(function() {
            $('input#title').unbind('keyup', update);
        });
    }
    
    $('textarea').tabby();
});
