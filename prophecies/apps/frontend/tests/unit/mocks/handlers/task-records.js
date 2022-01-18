import { rest } from 'msw'

export default [
  rest.get('/api/v1/task-records', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        links: {
          first: 'http://localhost/api/v1/task-records/?page%5Bnumber%5D=1',
          last: 'http://localhost/api/v1/task-records/?page%5Bnumber%5D=1',
          next: null,
          prev: null
        },
        data: [
          {
            type: 'TaskRecord',
            id: '3',
            attributes: {
              originalValue: 'La France',
              predictedValue: 'FRA',
              link: 'https://www.openstreetmap.org/search?query=La%20France',
              metadata: null,
              rounds: 3,
              saved: true,
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
          },
          {
            type: 'TaskRecord',
            id: '2',
            attributes: {
              originalValue: 'Germany',
              predictedValue: 'DE',
              link: 'https://www.openstreetmap.org/search?query=Germany',
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
              self: 'http://localhost/api/v1/task-records/2/'
            }
          },
          {
            type: 'TaskRecord',
            id: '1',
            attributes: {
              originalValue: 'fronce',
              predictedValue: 'France',
              link: 'https://www.openstreetmap.org/search?query=fronce',
              metadata: null,
              rounds: 3,
              saved: false,
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
          }
        ],
        included: [
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
              rounds: 3,
              taskRecordsCount: 1000,
              taskRecordsDoneCount: 500,
              userTaskRecordsCount: 300,
              userTaskRecordsDoneCount: 100,
              userProgressByRound: {
                1: 100,
                2: 25,
                3: 25
              },
              userProgress: 50,
              progress: 50,
              progressByRound: {
                1: 200,
                2: 100,
                3: 200
              }
            },
            relationships: {
              choiceGroup: {
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
  }),
  rest.get('/api/v1/task-records/3/relationships/actions', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        links: {
          first: 'http://localhost/api/v1/task-records/7/relationships/actions/?page%5Bnumber%5D=1',
          last: 'http://localhost/api/v1/task-records/7/relationships/actions/?page%5Bnumber%5D=1',
          next: null,
          prev: null
        },
        data: [
          {
            type: 'Action',
            id: '13',
            attributes: {
              verb: 'reviewed',
              data: null,
              public: true,
              description: null,
              timestamp: '2021-08-26T19:41:05.657206Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              actionObject: {
                data: {
                  type: 'Choice',
                  id: '1'
                }
              },
              target: {
                data: {
                  type: 'TaskRecordReview',
                  id: '388'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/actions/13/'
            }
          }
        ],
        included: [
          {
            type: 'Choice',
            id: '1',
            attributes: {
              name: 'Correct',
              value: 'correct',
              shortkeys: 'c',
              requireAlternativeValue: false
            }
          },
          {
            type: 'TaskRecordReview',
            id: '388',
            attributes: {
              status: 'DONE',
              note: ';)',
              alternativeValue: null
            },
            relationships: {
              checker: {
                data: {
                  type: 'User',
                  id: '9'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '3'
                }
              },
              taskRecord: {
                data: {
                  type: 'TaskRecord',
                  id: '7'
                }
              },
              history: {
                data: [
                  {
                    type: 'TaskRecordReview',
                    id: '388'
                  }
                ]
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-record-reviews/388/'
            }
          },
          {
            type: 'User',
            id: '2',
            attributes: {
              url: 'http://localhost/api/v1/users/2/',
              firstName: 'Django',
              lastName: '',
              username: 'django',
              email: 'support@icij.org',
              emailMd5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
              isStaff: true
            },
            links: {
              self: 'http://localhost/api/v1/users/2/'
            }
          }
        ],
        meta: {
          pagination: {
            page: 1,
            pages: 1,
            count: 1
          }
        }
      })
    )
  })
]
