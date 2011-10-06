$(function() {
    function initForms() {
        $("select, input:checkbox, input:radio, input:file, input:text, textarea, button, a.button").filter(':not(.uniform)').addClass('uniform').uniform();
    }
    
    function loadMore(e) {
        var link = this;
        
        $.get($(link).attr('href'), function(data) {
            $(link).before(data);
            initForms();
            $(link).remove();
        });
        
        return false;
    }

    window.setTimeout(function() {
        $('.message').fadeOut();
    }, 3000);
    
    initForms();

    $('body').delegate('.show-more', 'click', function(e) {
        loadMore.call(this, e);
        return false;
    });
    
    $(document).bind('scroll', function(e) {
        if($('.show-more:in-viewport').length) {
            loadMore.call($('.show-more:in-viewport').get(0), e);
        }
    });
});
