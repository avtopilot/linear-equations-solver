$(document).ready(function() {
  $('#equation').on('submit', function() {
    var $form;
    $form = $(this)

    $.ajax({
      url: $form.attr('action'),
      type: $form.attr('method'),
      data: $form.serialize(),
      complete: function(xhr, textStatus) {
      },
      success: function(data, textStatus, xhr) {
        $('#result').html(data);
      },
      error: function(xhr, textStatus, errorThrown) {
        alert('An error occurred!');
      }
    });
    return false;
  });
});