export function toUpperCaseForSingleChar (str = '') {
  if (str.length === 1) {
    return str.toUpperCase()
  }
  return str
}

export function metaKeyDisplay (str = '') {
  if (str.toLowerCase() === 'meta') {
    if (navigator.userAgent.toLowerCase().indexOf('mac os') !== -1) {
      return '⌘'
    }
    return 'Ctrl'
  }
  return str
}
