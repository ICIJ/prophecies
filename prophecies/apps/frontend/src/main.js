import { createCore } from '@/core'
import '@/main.scss'

if (process.env.NODE_ENV !== 'test' && window) {
  const prophecies = createCore()
  // Mount the core when it's ready
  prophecies.ready
    // Redirect to the error page
    .catch(error => {
      const { currentRoute } = prophecies.router
      // Unauthenticated error during initialization:
      // redirect the user to the login page
      if (error?.response?.status === 403 && currentRoute.name !== 'login') {
        prophecies.router.push({ name: 'login' })
      } else {
        prophecies.router.push({ name: 'error', params: { error } })
      }
    })
    .finally(() => {
      // Always end up mounting the app
      prophecies.mount()
    })
  // Register the core globally (so plugins can use it)
  window.prophecies = prophecies
}
