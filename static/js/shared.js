$(function() {
    var loading = false;
    
    function loadMore(e) {
        if(loading) {
            return false
        };

        loading = true;

        var link = this;
        $(link).fadeOut();

        $.get($(link).attr('href'), function(data) {
            $(link).before(data);
            initForms();
            $(link).remove();
            loading = false;
        });
        
        return false;
    }

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
