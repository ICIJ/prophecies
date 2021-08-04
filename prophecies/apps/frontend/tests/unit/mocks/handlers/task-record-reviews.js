import { rest } from 'msw'

export default [
  rest.get('/api/v1/task-record-reviews', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        links: {
          first: 'http://localhost/api/v1/task-record-reviews/?page%5Bnumber%5D=1',
          last: 'http://localhost/api/v1/task-record-reviews/?page%5Bnumber%5D=1',
          next: null,
          prev: null
        },
        data: [
          {
            type: 'TaskRecordReview',
            id: '38',
            attributes: {
              status: 'DONE',
              note: "I really don't know",
              alternative_value: '??'
            },
            relationships: {
              choice: {
                data: {
                  type: 'Choice',
                  id: '3'
                }
              },
              task_record: {
                data: {
                  type: 'TaskRecord',
                  id: '3'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-record-reviews/38/'
            }
          },
          {
            type: 'TaskRecordReview',
            id: '37',
            attributes: {
              status: 'DONE',
              note: 'This is bad',
              alternative_value: 'FRA'
            },
            relationships: {
              choice: {
                data: {
                  type: 'Choice',
                  id: '2'
                }
              },
              task_record: {
                data: {
                  type: 'TaskRecord',
                  id: '1'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-record-reviews/37/'
            }
          }
        ],
        included: [
          {
            type: 'Choice',
            id: '1',
            attributes: {
              name: 'Correct',
              value: 'correct'
            }
          },
          {
            type: 'Choice',
            id: '2',
            attributes: {
              name: 'Incorrect',
              value: 'incorrect'
            }
          },
          {
            type: 'Choice',
            id: '3',
            attributes: {
              name: 'Unkown',
              value: 'unkown'
            }
          },
          {
            type: 'TaskRecord',
            id: '1',
            attributes: {
              original_value: 'fronce',
              predicted_value: 'France',
              link: 'https://www.openstreetmap.org/search?query=fronce',
              metadata: null,
              rounds: 3,
              status: 'DONE'
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '1'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-records/1/'
            }
          },
          {
            type: 'TaskRecord',
            id: '3',
            attributes: {
              original_value: 'La France',
              predicted_value: 'FRA',
              link: 'https://www.openstreetmap.org/search?query=La%20France',
              metadata: null,
              rounds: 3,
              status: 'ASSIGNED'
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '1'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-records/3/'
            }
          }
        ],
        meta: {
          pagination: {
            page: 1,
            pages: 1,
            count: 2
          }
        }
      })
    )
  })
]
