'use strict';
(function () {
  if (!django) {
    return
  }

  const $ = django.jQuery

  $.fn.adminSelectAutosubmit = function () {
    $.each(this, (i, element) => {
      $(element).on('change', function () {
        const option = this.options[this.selectedIndex].value
        window.location = window.location.pathname + option
      })
    })
    return this
  }

  $(function () {
    $('.admin-select-autosubmit').adminSelectAutosubmit()
  })
})()