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
    let userAgentGetter

    beforeAll(() => {
      userAgentGetter = jest.spyOn(window.navigator, 'userAgent', 'get')
    })

    afterAll(() => {
      jest.restoreAllMocks()
    })

    it('should convert the "meta" key work to "⌘" on Mac', () => {
      userAgentGetter.mockReturnValue('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0')
      expect(metaKeyDisplay('meta')).toBe('⌘')
      userAgentGetter.mockReturnValue('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15')
      expect(metaKeyDisplay('meta')).toBe('⌘')
    })

    it('should convert the "meta" key work to "Ctrl" on Windows', () => {
      userAgentGetter.mockReturnValue('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
      userAgentGetter.mockReturnValue('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
    })

    it('should convert the "meta" key work to "Ctrl" on Linux', () => {
      userAgentGetter.mockReturnValue('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
      userAgentGetter.mockReturnValue('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
    })

    it('should convert the "meta" key work to "Ctrl" by default', () => {
      userAgentGetter.mockReturnValue('Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
      userAgentGetter.mockReturnValue('Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)')
      expect(metaKeyDisplay('meta')).toBe('Ctrl')
    })
  })
})
