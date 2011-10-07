$(function() {
    //hide messages
    window.setTimeout(function() {
        $('.message').fadeOut();
    }, 3000);
    
    //initialize for styling
    (function initForms() {
        $("select, input:checkbox, input:radio, input:file, input:text, textarea, button, a.button").filter(':not(.uniform)').addClass('uniform').uniform();
    }());
});
