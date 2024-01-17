'use strict'

(function () {
  const spinnerHtml = `
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 100 100"
      class="admin-submit-spinner">
      <circle cx="50" cy="50" fill="none" stroke="currentColor" stroke-width="10" r="35" stroke-dasharray="164.93361431346415 56.97787143782138">
        <animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" values="0 50 50360 50 50" keyTimes="01"></animateTransform>
      </circle>
    </svg>
  `

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', function () {
        // Freeze all submit buttons
        this.querySelectorAll('[type=submit]').forEach(submitButton => {
          submitButton.disabled = true
        })

        // Get the submitting target
        const activeElement = document.activeElement
        const isSubmitButton = activeElement.tagName === 'BUTTON' && activeElement.type === 'submit'
        const isInSubmitRow = !!activeElement.closest('.submit-row')

        // In the submit row (change form),
        // the button will be wrapped and
        // the spinner put in absolute position.
        if (isInSubmitRow) {
          const wrapper = document.createElement('span')
          wrapper.className = 'position-relative'
          activeElement.parentNode.insertBefore(wrapper, activeElement)
          wrapper.appendChild(activeElement)
          activeElement.insertAdjacentHTML('afterend', spinnerHtml)

        // In other <button>
        // the spinner will just replace the content.
        } else if (isSubmitButton) {
          activeElement.innerHTML = spinnerHtml
        }
      })
    })
  })
})()
