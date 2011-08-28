$(function() {
  $("select, input:checkbox, input:radio, input:file, input:text, textarea, button, a.button").uniform();

  window.setTimeout(function() {
      $('.message').fadeOut();
  }, 3000);
});