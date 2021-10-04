'use strict';
(function () {
  const $ = django.jQuery

  $.fn.adminSelect2 = function () {
    $.each(this, (i, element) => $(element).select2())
    return this
  }

  $(function () {
    // Initialize all select2 widgets except the one in the template
    // form used when a new formset is added.
    $('.admin-select2').not('[name*=__prefix__]').adminSelect2()
  })
})()