function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
      }
    : null
}

export function textContrast(n) {
  const rgb = hexToRgb(n)
  if (!rgb) {
    return '#071111' // $body-color
  }
  const colorbrightness = Math.round(rgb.r * 299 + rgb.g * 587 + (rgb.b * 114) / 1000)
  const col = 330
  const lightcolor = Math.round(col * 299 + col * 587 + (col * 114) / 1000) / 2

  if (Math.abs(colorbrightness) < lightcolor) {
    return 'white'
  }

  return '#071111' // $body-color
}
