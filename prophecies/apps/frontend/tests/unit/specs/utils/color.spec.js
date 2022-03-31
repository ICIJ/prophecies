import { textContrast } from '@/utils/color'

describe('utils/color', () => {
  describe('textContrast', () => {
    it('should return black color when color format is not hexadecimal', () => {
      expect(textContrast('foo')).toBe('black')
      expect(textContrast('#FFFFFF')).toBe('black')
    })
    it('should return black color when color is to light', () => {
      expect(textContrast('#FFFFFF')).toBe('black')
    })
    it('should return white color when color is to dark', () => {
      expect(textContrast('#000000')).toBe('white')
    })
  })
})
