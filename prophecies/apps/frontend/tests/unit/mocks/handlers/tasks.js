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
              progress: 40,
              progressByRound: {
                1: 50,
                2: 25,
                3: 30
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
              },
              checkers: {
                meta: {
                  count: 1
                },
                data: [
                  {
                    type: 'User',
                    id: '2'
                  }
                ]
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
              userProgress: 45,
              progress: 60,
              progressByRound: {
                1: 50,
                2: 25,
                3: 25
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
              },
              checkers: {
                meta: {
                  count: 1
                },
                data: [
                  {
                    type: 'User',
                    id: '2'
                  }
                ]
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
              },
              alternativeValues: {
                meta: {
                  count: 2
                },
                data: [
                  {
                    type: 'AlternativeValue',
                    id: '10'
                  },
                  {
                    type: 'AlternativeValue',
                    id: '11'
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
          },
          {
            type: 'AlternativeValue',
            id: '10',
            attributes: {
              name: 'Albania (ALB)',
              value: 'ALB'
            }
          },
          {
            type: 'AlternativeValue',
            id: '11',
            attributes: {
              name: 'Algeria (DZA)',
              value: 'DZA'
            }
          }
        ]
      })
    )
  }),
  rest.get('/api/v1/tasks/1/', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: {
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
            progress: 40,
            progressByRound: {
              1: 50,
              2: 25,
              3: 30
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
            },
            checkers: {
              meta: {
                count: 1
              },
              data: [
                {
                  type: 'User',
                  id: '2'
                }
              ]
            }
          },
          links: {
            self: 'http://localhost/api/v1/tasks/1/'
          }
        },
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
              },
              alternativeValues: {
                meta: {
                  count: 2
                },
                data: [
                  {
                    type: 'AlternativeValue',
                    id: '10'
                  },
                  {
                    type: 'AlternativeValue',
                    id: '11'
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
          },
          {
            type: 'AlternativeValue',
            id: '10',
            attributes: {
              name: 'Albania (ALB)',
              value: 'ALB'
            }
          },
          {
            type: 'AlternativeValue',
            id: '11',
            attributes: {
              name: 'Algeria (DZA)',
              value: 'DZA'
            }
          }
        ]
      })
    )
  })
]
