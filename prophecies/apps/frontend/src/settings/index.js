export default {
  adminUrl: '/admin',
  avatarUrlTemplate: 'https://www.gravatar.com/avatar/{{ emailMd5 }}',
  apiUrl: '/api/v1',
  defaultLocale: 'en',
  helpLink: 'https://github.com/ICIJ/prophecies/issues/new',
  locales: [
    {
      key: 'en',
      label: 'English'
    },
    {
      key: 'es',
      label: 'Español'
    },
    {
      key: 'fr',
      label: 'Français'
    }
  ],
  loginUrl: '/login/provider/?next=/',
  logoutUrl: '/admin/logout/?next=/',
  templateInterpolate: /{{ ?([\s\S]+?) ?}}/g,
  variantsMap: {
    success: 'success',
    ok: 'success',
    done: 'success',
    correct: 'success',
    danger: 'danger',
    error: 'danger',
    fail: 'danger',
    failed: 'danger',
    failure: 'danger',
    incorrect: 'danger',
    info: 'info',
    pending: 'info',
    queued: 'info',
    running: 'info',
    warning: 'warning',
    cancelled: 'warning'
  }
}
