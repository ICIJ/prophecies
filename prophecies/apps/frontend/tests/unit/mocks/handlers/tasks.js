// src/mocks/handlers.js
import { rest } from 'msw'

export default [
  rest.get('/api/v1/tasks', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'Task',
            id: '1',
            attributes: {
              colors: [
                '#60245c',
                '#80307b',
                '#a03c9a'
              ],
              description: 'A collection of adresses to fact check.',
              name: 'Addresses',
              priority: 1,
              user_progress_by_round: {
                1: 0,
                2: 100.0,
                3: 0
              },
              progress_by_round: {
                1: 50.0,
                2: 100.0,
                3: 50.0
              },
              progress: 50.0,
              rounds: 3
            },
            relationships: {
              choice_group: {
                data: {
                  type: 'ChoiceGroup',
                  id: '1'
                }
              },
              project: {
                data: {
                  type: 'Project',
                  id: '1'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/tasks/1/'
            }
          },
          {
            type: 'Task',
            id: '2',
            attributes: {
              colors: [
                '#9e5e00',
                '#d37d00',
                '#ff9b09'
              ],
              description: 'A list of shop to check',
              name: 'Shops',
              priority: 1,
              user_progress_by_round: {
                1: 0,
                2: 0,
                3: 0
              },
              progress_by_round: {
                1: 0,
                2: 0,
                3: 0
              },
              progress: 100,
              rounds: 3
            },
            relationships: {
              choice_group: {
                data: {
                  type: 'ChoiceGroup',
                  id: '1'
                }
              },
              project: {
                data: {
                  type: 'Project',
                  id: '1'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/tasks/2/'
            }
          }
        ],
        included: [
          {
            type: 'ChoiceGroup',
            id: '1',
            attributes: {
              name: 'Is it correct?'
            },
            relationships: {
              choices: {
                meta: {
                  count: 3
                },
                data: [
                  {
                    type: 'Choice',
                    id: '1'
                  },
                  {
                    type: 'Choice',
                    id: '2'
                  },
                  {
                    type: 'Choice',
                    id: '3'
                  }
                ]
              }
            }
          },
          {
            type: 'Project',
            id: '1',
            attributes: {
              name: 'Chronos'
            },
            relationships: {
              creator: {
                data: {
                  type: 'User',
                  id: '2'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/projects/1/'
            }
          }
        ]
      })
    )
  })
]
