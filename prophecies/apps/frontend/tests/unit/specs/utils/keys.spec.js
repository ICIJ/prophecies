import { toUpperCaseForSingleChar, metaKeyDisplay } from '@/utils/keys'

describe('utils/keys', () => {
  describe('toUpperCaseForSingleChar', () => {
    it('should convert a single character to uppercase', () => {
      expect(toUpperCaseForSingleChar('a')).toBe('A')
      expect(toUpperCaseForSingleChar('b')).toBe('B')
      expect(toUpperCaseForSingleChar('c')).toBe('C')
    })

    it('should not convert several characters to uppercase', () => {
      expect(toUpperCaseForSingleChar('foo')).toBe('foo')
      expect(toUpperCaseForSingleChar('bar')).toBe('bar')
      expect(toUpperCaseForSingleChar('baz')).toBe('baz')
    })
  })

  describe('metaKeyDisplay', () => {
    let platformGetter = null

    beforeAll(() => {
      platformGetter = jest.spyOn(window.navigator, 'platform', 'get')
    })

    afterAll(() => {
      jest.restoreAllMocks()
    })

    it('should convert the "meta" key work to "⌘" on Mac', () => {
      platformGetter.mockReturnValue('Mac OS')
      expect(metaKeyDisplay('meta')).toBe('⌘')
      platformGetter.mockReturnValue('Mac OS X')
      expect(metaKeyDisplay('meta')).toBe('⌘')
    })

    it('should convert the "meta" key work to "Ctrl" on Windows', () => {
      platformGetter.mockReturnValue('Windows XP')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
      platformGetter.mockReturnValue('Windows 7')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
      platformGetter.mockReturnValue('Windows 10')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
    })

    it('should convert the "meta" key work to "Ctrl" on Linux', () => {
      platformGetter.mockReturnValue('Linux')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
      platformGetter.mockReturnValue('Linux Ubuntu')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
    })

    it('should convert the "meta" key work to "Ctrl" by default', () => {
      platformGetter.mockReturnValue('Future OS')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
      platformGetter.mockReturnValue('No OS')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
    })
  })
})
