// src/mocks/handlers.js
import { rest } from 'msw'

export const handlers = [

  rest.get('/api/v1/settings', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'Setting',
            attributes: {
              key: 'appName',
              value: 'Data Fact Check'
            }
          },
          {
            type: 'Setting',
            attributes: {
              key: 'orgName',
              value: 'ICIJ.org'
            }
          },
          {
            type: 'Setting',
            attributes: {
              key: 'appVersion',
              value: '0.4.6'
            }
          }
        ]
      })
    )
  }),

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
  }),

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
              suggested_value: 'France',
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
              suggested_value: 'FRA',
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
  }),

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
              original_value: 'La France',
              suggested_value: 'FRA',
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
          },
          {
            type: 'TaskRecord',
            id: '1',
            attributes: {
              original_value: 'fronce',
              suggested_value: 'France',
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

  rest.get('/api/v1/users', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'User',
            id: 2,
            attributes: {
              url: 'http://localhost/api/v1/users/2/',
              first_name: 'Django',
              last_name: '',
              username: 'django',
              email: 'support@icij.org',
              email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
              is_staff: true
            },
            links: {
              self: 'http://localhost:9009/api/v1/users/2/'
            }
          }
        ]
      })
    )
  }),

  rest.get('/api/v1/users/me/', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: {
          type: 'User',
          id: 2,
          attributes: {
            url: 'http://localhost/api/v1/users/2/',
            first_name: 'Django',
            last_name: '',
            username: 'django',
            email: 'support@icij.org',
            email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
            is_staff: true
          },
          links: {
            self: 'http://localhost:9009/api/v1/users/2/'
          }
        }
      })
    )
  })
]
