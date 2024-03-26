import '@/store'
import UserNotification from '@/models/UserNotification'

describe('UserNotification', () => {
  beforeAll(async () => {
    await UserNotification.api().get()
  })

  afterAll(() => {
    UserNotification.deleteAll()
  })

  it('should have created 2 notification', async () => {
    expect(UserNotification.all()).toHaveLength(2)
  })

  it('should have one read notification', async () => {
    expect(UserNotification.find('4').read).toBeTruthy()
  })

  it('should have one unread notification', async () => {
    expect(UserNotification.find('1').read).toBeFalsy()
  })

  it('should have one user object as recipient', async () => {
    const { recipient } = UserNotification.query().with('recipient').find('1')
    expect(recipient.id).toBe('2')
    expect(recipient.username).toBe('django')
  })

  it('should have one action object', async () => {
    const { action } = UserNotification.query().with('action').find('1')
    expect(action.id).toBe('86')
    expect(action.verb).toBe('mentioned')
  })

  it('should have one action object and its nested actionObject', async () => {
    const {
      action: { actionObject }
    } = UserNotification.query().with('action').with('action.actionObject').find('4')
    expect(actionObject.id).toBe('38')
  })
})
