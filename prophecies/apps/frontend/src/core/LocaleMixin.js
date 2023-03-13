/**
 Mixin class extending the core to add helpers to manage the internationalization.
 @mixin LocaleMixin
 @typicalname prophecies
 */

const LocaleMixin = superclass => class extends superclass {
  /**
   * Set the i18n language from the locale
   * @param {String} locale - Locale code to load
   * @memberof LocaleMixin.prototype
   */
  setI18nLanguage(locale) {
    this.i18n.locale = locale
    return locale
  }

  /**
   * Load the application language from the locale
   * @param {String} locale - Locale code to load
   * @memberof LocaleMixin.prototype
   */
  loadLocale(locale) {
    if (this.loadedLocales === undefined) {
      this.loadedLocales = []
    }
    if (this.i18n.locale !== locale) {
      if (!this.loadedLocales.includes(locale)) {
        return import(/* webpackChunkName: "[request]" */ '@/messages/' + locale + '.json').then(messages => {
          this.i18n.setLocaleMessage(locale, messages.default)
          this.loadedLocales.push(locale)
          return this.setI18nLanguage(locale)
        })
      }
      return Promise.resolve(this.setI18nLanguage(locale))
    }
    return Promise.resolve(locale)
  }
}

export default LocaleMixin
