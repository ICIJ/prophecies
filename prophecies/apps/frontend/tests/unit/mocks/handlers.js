// src/mocks/handlers.js
import { rest } from 'msw'

export const handlers = [

  rest.get('/api/v1/settings', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          key: 'appName',
          value: 'Data Fact Check'
        },
        {
          key: 'orgName',
          value: 'ICIJ.org'
        },
        {
          key: 'appVersion',
          value: '0.4.6'
        }
      ])
    )
  }),

  rest.get('/api/v1/task-records', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json(
        [
          {
            id: 1,
            url: 'http://localhost/api/v1/task-records/1/',
            task: {
              id: 1,
              url: 'http://localhost/api/v1/tasks/1/',
              choice_group: {
                id: 1,
                name: 'Is it correct?',
                choices: [
                  {
                    id: 1,
                    name: 'Correct',
                    value: 'correct'
                  },
                  {
                    id: 2,
                    name: 'Incorrect',
                    value: 'incorrect'
                  },
                  {
                    id: 3,
                    name: 'Unkown',
                    value: 'unkown'
                  }
                ]
              },
              colors: [
                '#60245c',
                '#80307b',
                '#a03c9a'
              ],
              description: 'A collection of adresses to fact check.',
              name: 'Addresses',
              project: {
                id: 1,
                url: 'http://localhost/api/v1/projects/1/',
                creator: {
                  id: 2,
                  url: 'http://localhost/api/v1/users/2/',
                  first_name: 'Django',
                  last_name: '',
                  username: 'django',
                  email: 'support@icij.org',
                  email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
                  is_staff: true
                },
                name: 'Aladdin'
              },
              priority: 1,
              rounds: 3
            },
            original_value: 'fronce',
            suggested_value: 'France',
            link: 'https://www.openstreetmap.org/search?query=fronce',
            metadata: null,
            rounds: 2,
            status: 'ASSIGNED'
          },
          {
            id: 3,
            url: 'http://localhost/api/v1/task-records/3/',
            task: {
              id: 1,
              url: 'http://localhost/api/v1/tasks/1/',
              choice_group: {
                id: 1,
                name: 'Is it correct?',
                choices: [
                  {
                    id: 1,
                    name: 'Correct',
                    value: 'correct'
                  },
                  {
                    id: 2,
                    name: 'Incorrect',
                    value: 'incorrect'
                  },
                  {
                    id: 3,
                    name: 'Unkown',
                    value: 'unkown'
                  }
                ]
              },
              colors: [
                '#60245c',
                '#80307b',
                '#a03c9a'
              ],
              description: 'A collection of adresses to fact check.',
              name: 'Addresses',
              project: {
                id: 1,
                url: 'http://localhost/api/v1/projects/1/',
                creator: {
                  id: 2,
                  url: 'http://localhost/api/v1/users/2/',
                  first_name: 'Django',
                  last_name: '',
                  username: 'django',
                  email: 'support@icij.org',
                  email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
                  is_staff: true
                },
                name: 'Aladdin'
              },
              priority: 1,
              rounds: 3
            },
            original_value: 'La France',
            suggested_value: 'FRA',
            link: 'https://www.openstreetmap.org/search?query=La%20France',
            metadata: null,
            rounds: 2,
            status: 'ASSIGNED'
          }
        ]
      )
    )
  }),

  rest.get('/api/v1/users', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: 2,
          url: 'http://localhost/api/v1/users/2/',
          first_name: 'Django',
          last_name: '',
          username: 'django',
          email: 'support@icij.org',
          email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
          is_staff: true
        }
      ])
    )
  }),

  rest.get('/api/v1/users/me.json', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        id: 2,
        url: 'http://localhost/api/v1/users/2/',
        first_name: 'Django',
        last_name: '',
        username: 'django',
        email: 'support@icij.org',
        email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
        is_staff: true
      })
    )
  })
]
