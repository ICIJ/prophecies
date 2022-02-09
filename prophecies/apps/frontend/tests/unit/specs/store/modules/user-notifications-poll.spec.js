import UserNotification from '@/models/UserNotification'
import { createStore } from '@/store'


describe('userNotificationsPoll', () => {
  let store 

  // Ensure we advance timers and run all pending job
  // in the PromiseJobs queue.
  function advanceTimersByTimeAndFlushPromises (ms) {
    jest.advanceTimersByTime(ms)
    return new Promise(done => jest.requireActual("timers").setTimeout(done, 200))
  }
  
  beforeEach(() => {
    jest.useFakeTimers()
    store = createStore()
  })

  afterAll(() => {
    jest.useRealTimers()
  })

  it('should instantiate a state object', () => {
    expect(store.state.userNotificationsPoll).toBeInstanceOf(Object)
  })

  it('should fetch notifications with an action', async () => {
    expect(UserNotification.query().count()).toBe(0)
    await store.dispatch('userNotificationsPoll/fetch')
    expect(UserNotification.query().count()).not.toBe(0)
  })

  it('should count the number of time notifications were fetched', async () => {
    expect(store.state.userNotificationsPoll.fetchs).toBe(0)
    await store.dispatch('userNotificationsPoll/fetch')
    expect(store.state.userNotificationsPoll.fetchs).toBe(1)
    await store.dispatch('userNotificationsPoll/fetch')
    expect(store.state.userNotificationsPoll.fetchs).toBe(2)
  })

  it('should plan a fetch of the notifications', () => {
    expect(store.state.userNotificationsPoll.pollId).toBeFalsy()
    store.dispatch('userNotificationsPoll/startPoll')
    expect(store.state.userNotificationsPoll.pollId).toBeTruthy()
  })


  it('should plan a fetch of the notifications and get them right away', async () => {
    expect(store.state.userNotificationsPoll.pollId).toBeFalsy()
    store.dispatch('userNotificationsPoll/startPollAndFetch')
    expect(store.state.userNotificationsPoll.pollId).toBeTruthy()
    await advanceTimersByTimeAndFlushPromises(0)
    expect(store.state.userNotificationsPoll.fetchs).toBe(1)
  })

  it('should fetch notifications 1 time in 15 secondes', async () => {
    store.dispatch('userNotificationsPoll/startPoll')
    await advanceTimersByTimeAndFlushPromises(1e3 * 15)
    expect(store.state.userNotificationsPoll.fetchs).toBe(1)
  })
  
  it('should fetch notifications 2 times in 25 secondes', async () => {
    store.dispatch('userNotificationsPoll/startPoll')
    await advanceTimersByTimeAndFlushPromises(1e3 * 25)
    expect(store.state.userNotificationsPoll.fetchs).toBe(2)
  })

  it('should not plan fetch notifications twice', async () => {
    store.dispatch('userNotificationsPoll/startPoll')
    store.dispatch('userNotificationsPoll/startPoll')
    await advanceTimersByTimeAndFlushPromises(1e3 * 15)
    expect(store.state.userNotificationsPoll.fetchs).toBe(1)
  })

  it('should clear fetch notifications', async () => {
    store.dispatch('userNotificationsPoll/startPoll')
    await advanceTimersByTimeAndFlushPromises(1e3 * 15)
    expect(store.state.userNotificationsPoll.fetchs).toBe(1)
    store.dispatch('userNotificationsPoll/clearPoll')
    await advanceTimersByTimeAndFlushPromises(1e3 * 15)
    expect(store.state.userNotificationsPoll.fetchs).toBe(1)
  })

  it('should set "fetched" getter as true after a 15 seconds', async () => {
    store.dispatch('userNotificationsPoll/startPoll')
    await advanceTimersByTimeAndFlushPromises(1e3 * 15)
    expect(store.getters['userNotificationsPoll/fetched']).toBeTruthy()
  })

  it('should not set "fetched" getter as true after a 1 second', async () => {
    store.dispatch('userNotificationsPoll/startPoll')
    await advanceTimersByTimeAndFlushPromises(1e3)
    expect(store.getters['userNotificationsPoll/fetched']).toBeFalsy()
  })
})
