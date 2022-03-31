import { textContrast } from '@/utils/color'

describe('utils/color', () => {
  describe('textContrast', () => {
    it('should return body color when color format is not hexadecimal', () => {
      expect(textContrast('foo')).toBe('#071111')
      expect(textContrast('#FFFFFF')).toBe('#071111')
    })
    it('should return body color when color is to light', () => {
      expect(textContrast('#FFFFFF')).toBe('#071111')
    })
    it('should return white color when color is to dark', () => {
      expect(textContrast('#000000')).toBe('white')
    })
  })
})
