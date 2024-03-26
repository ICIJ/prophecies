import { slugger } from '@/utils/strings'
import settings from '@/settings'

export function toVariant(string = '', defaultVariant = 'secondary', prefix = '') {
  return prefix + (settings.variantsMap[slugger(string).toLowerCase()] || defaultVariant)
}

export function toVariantColor(string = '', defaultVariant = 'darker') {
  const variant = toVariant(string, defaultVariant)
  const style = getComputedStyle(document.body)
  return style.getPropertyValue(`--${variant}`) || '#eee'
}
