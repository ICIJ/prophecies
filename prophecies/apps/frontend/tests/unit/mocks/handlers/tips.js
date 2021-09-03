import { rest } from 'msw'

export default [
  rest.get('/api/v1/tips', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'Tip',
            id: '4',
            attributes: {
              name: 'tip for test 4',
              description: 'test description 4',
              createdAt: '2021-09-02T12:58:16.113007Z',
              updatedAt: '2021-09-02T12:58:16.113038Z'
            },
            relationships: {
              project: {
                data: {
                  type: 'Project',
                  id: '1'
                }
              },
              creator: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              task: {
                data: {
                  type: 'Task',
                  id: '2'
                }
              }
            }
          },
          {
            type: 'Tip',
            id: '3',
            attributes: {
              name: 'tip for test 3',
              description: 'test description 3',
              createdAt: '2021-09-02T12:58:16.113007Z',
              updatedAt: '2021-09-02T12:58:16.113038Z'
            },
            relationships: {
              project: {
                data: {
                  type: 'Project',
                  id: '1'
                }
              },
              creator: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              task: {
                data: {
                  type: 'Task',
                  id: '2'
                }
              }
            }
          }
        ],
        included: [
          {
           type: 'Project',
           id: '1',
           attributes: {
             name: 'Aladdin'
           },
           relationships: {
             creator: {
               data: {
                 type: 'User',
                 id: '1'
               }
             }
           },
           links: {
             self: 'http://localhost/api/v1/projects/1/'
           }
         },
         {
          type: 'Task',
          id: '2',
          attributes: {
            colors: [
              '#25605e',
              '#31807d',
              '#3da09c'
            ],
            description: 'Checking more stuff',
            name: 'Another Task',
            priority: 1,
            rounds: 3,
            taskRecordsCount: 0,
            taskRecordsDoneCount: 0,
            userTaskRecordsCount: 0,
            userTaskRecordsDoneCount: 0,
            userProgressByRound: {
              1: 0,
              2: 0,
              3: 0
            },
            userProgress: 100,
            progress: 100,
            progressByRound: {
              1: 0,
              2: 0,
              3: 0
            }
            },
            relationships: {
              choiceGroup: {
                data: {
                  type: 'ChoiceGroup',
                  id: '1'
                }
              },
              checkers: {
                meta: {
                  count: 2
                },
                data: [
                  {
                    type: 'User',
                    id: '1'
                  },
                  {
                    type: 'User',
                    id: '2'
                  }
                ]
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
          },
          {
            type: 'User',
            id: '1',
            attributes: {
              firstName: 'Django',
              lastName: '',
              username: 'django',
              emailMd5: 'b6e60d14b351a879090a400872b89ec1',
              isStaff: true,
            },
            links: {
              self: 'http://localhost/api/v1/users/1/'
            }
          }
        ]
      })
    )
  })
]
