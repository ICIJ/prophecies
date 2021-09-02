import '@/store'
import Notification from '@/models/Notification'

describe('Notification', () => {
  beforeAll(async () => {
    await Notification.api().get()
  })

  afterAll(() => {
    Notification.deleteAll()
  })

  it('should have created 2 notification', async () => {
    expect(Notification.all()).toHaveLength(2)
  })

  it('should have one read notification', async () => {
    expect(Notification.find('4').read).toBeTruthy()
  })

  it('should have one unread notification', async () => {
    expect(Notification.find('1').read).toBeFalsy()
  })

  it('should have one user object as recipient', async () => {
    const { recipient } = Notification.query().with('recipient').find('1')
    expect(recipient.id).toBe('2')
    expect(recipient.username).toBe('django')
  })

  it('should have one action object', async () => {
    const { action } = Notification.query().with('action').find('1')
    expect(action.id).toBe('86')
    expect(action.verb).toBe('mentioned')
  })

  it('should have one action object and its nested actionObject', async () => {
    const { action: { actionObject } } = Notification.query()
      .with('action')
      .with('action.actionObject')
      .find('4')
    expect(actionObject.id).toBe('38')
  })
})
