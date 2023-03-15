import { server } from './mocks/server'

// Establish API mocking before all tests.
beforeAll(() => server.listen())

// so they don't affect other tests.
afterEach(() => server.resetHandlers())

// Clean up after the tests are finished.
afterAll(() => server.close())
