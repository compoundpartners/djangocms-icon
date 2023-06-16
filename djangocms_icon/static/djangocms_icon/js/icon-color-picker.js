jQuery(document).ready(function($){
  $('.js-icon .color-picker').change(function() {
    $(this).parents('.js-icon').find('.js-iconcolor').val($(this).val()).trigger('change');
  });
});
