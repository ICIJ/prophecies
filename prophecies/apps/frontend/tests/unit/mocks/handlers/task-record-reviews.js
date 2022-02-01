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
              alternativeValue: '??',
              taskId: '1'
            },
            relationships: {
              choice: {
                data: {
                  type: 'Choice',
                  id: '3'
                }
              },
              taskRecord: {
                data: {
                  type: 'TaskRecord',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              collaborators: {
                data: []
              },
              history: {
                data: [
                  {
                    type: 'TaskRecordReview',
                    id: '38'
                  }
                ]
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
              alternativeValue: 'FRA',
              taskId: '1'
            },
            relationships: {
              choice: {
                data: {
                  type: 'Choice',
                  id: '2'
                }
              },
              taskRecord: {
                data: {
                  type: 'TaskRecord',
                  id: '1'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              collaborators: {
                data: []
              },
              history: {
                data: [
                  {
                    type: 'TaskRecordReview',
                    id: '37'
                  }
                ]
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-record-reviews/37/'
            }
          },
          {
            type: 'TaskRecordReview',
            id: '36',
            attributes: {
              status: 'PENDING',
              note: '',
              alternativeValue: '',
              taskId: '2'
            },
            relationships: {
              choice: {
                data: null
              },
              taskRecord: {
                data: {
                  type: 'TaskRecord',
                  id: '1'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-record-reviews/285/'
            }
          },
          {
            type: 'TaskRecordReview',
            id: '25',
            attributes: {
              status: 'DONE',
              note: "I really don't know",
              alternativeValue: '??',
              taskId: '2'
            },
            relationships: {
              choice: {
                data: {
                  type: 'Choice',
                  id: '3'
                }
              },
              taskRecord: {
                data: {
                  type: 'TaskRecord',
                  id: '5'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              collaborators: {
                data: []
              },
              history: {
                data: [
                  {
                    type: 'TaskRecordReview',
                    id: '25'
                  }
                ]
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-record-reviews/25/'
            }
          },
          {
            type: 'TaskRecordReview',
            id: '24',
            attributes: {
              status: 'PENDING',
              note: "I really don't know",
              alternativeValue: '??',
              taskId: '2'
            },
            relationships: {
              choice: {
                data: null
              },
              taskRecord: {
                data: {
                  type: 'TaskRecord',
                  id: '4'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              collaborators: {
                data: []
              },
              history: {
                data: [
                  {
                    type: 'TaskRecordReview',
                    id: '24'
                  }
                ]
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-record-reviews/24/'
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
              originalValue: 'fronce',
              predictedValue: 'France',
              locked: false,
              link: 'https://www.openstreetmap.org/search?query=fronce',
              metadata: null,
              rounds: 3,
              status: 'ASSIGNED'
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '2'
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
              originalValue: 'La France',
              predictedValue: 'FRA',
              locked: true,
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
              },
              lockedBy: {
                data: '2'
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-records/3/'
            }
          },
          {
            type: 'TaskRecord',
            id: '4',
            attributes: {
              originalValue: 'La France',
              predictedValue: 'FRA',
              locked: false,
              link: 'https://www.openstreetmap.org/search?query=La%20France',
              metadata: null,
              rounds: 3,
              status: 'ASSIGNED'
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '2'
                }
              },
              lockedBy: {
                data: '2'
              },
              bookmarkedBy: {
                data: [
                  {
                    type: 'User',
                    id: '1'
                  }
                ],
                meta: {
                  count: 1
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-records/4/'
            }
          },
          {
            type: 'TaskRecord',
            id: '5',
            attributes: {
              originalValue: 'La France',
              predictedValue: 'FRA',
              locked: false,
              link: 'https://www.openstreetmap.org/search?query=La%20France',
              metadata: null,
              rounds: 3,
              status: 'ASSIGNED'
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '2'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/task-records/5/'
            }
          },
          {
            type: 'User',
            id: 2,
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
            count: 3
          }
        }
      })
    )
  })
]
