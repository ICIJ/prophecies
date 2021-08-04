import { setupServer } from 'msw/node'
import { join } from 'path'
import { readdirSync } from 'fs'

// Collect all handlers in the handlers directory
const normalizedPath = join(__dirname, 'handlers')
const handlers = readdirSync(normalizedPath).reduce((handlers, file) => {
  const { default: fileHandlers } = require(join(normalizedPath, file))
  return [...handlers, ...fileHandlers]
}, [])

// This configures a request mocking server with the given request handlers.
export const server = setupServer(...handlers)
export { rest } from 'msw'
