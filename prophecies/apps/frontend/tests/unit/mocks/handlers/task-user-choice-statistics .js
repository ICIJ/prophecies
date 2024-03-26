import { rest } from 'msw'

export default [
  rest.get('/api/v1/task-user-choice-statistics', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'TaskChoiceStatistics',
            id: '12',
            attributes: {
              round: 1,
              count: 39
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '1'
                }
              }
            }
          },
          {
            type: 'TaskChoiceStatistics',
            id: '13',
            attributes: {
              round: 1,
              count: 1
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '2'
                }
              }
            }
          },
          {
            type: 'TaskChoiceStatistics',
            id: '14',
            attributes: {
              round: 1,
              count: 3
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '3'
                }
              }
            }
          },
          {
            type: 'TaskChoiceStatistics',
            id: '16',
            attributes: {
              round: 2,
              count: 1
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '1'
                }
              }
            }
          },
          {
            type: 'TaskChoiceStatistics',
            id: '17',
            attributes: {
              round: 2,
              count: 1
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '3'
                }
              }
            }
          },
          {
            type: 'TaskChoiceStatistics',
            id: '27',
            attributes: {
              round: 3,
              count: 1
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '3'
                }
              }
            }
          },
          {
            type: 'TaskChoiceStatistics',
            id: '28',
            attributes: {
              round: 1,
              count: 3
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '1'
                }
              }
            }
          },
          {
            type: 'TaskChoiceStatistics',
            id: '29',
            attributes: {
              round: 1,
              count: 1
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '2'
                }
              }
            }
          },
          {
            type: 'TaskChoiceStatistics',
            id: '30',
            attributes: {
              round: 1,
              count: 1
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '3'
                }
              }
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
            type: 'Choice',
            id: '2',
            attributes: {
              name: 'Incorrect',
              value: 'incorrect',
              shortkeys: 'i',
              requireAlternativeValue: true
            }
          },
          {
            type: 'Choice',
            id: '3',
            attributes: {
              name: "Don't know",
              value: 'dontknow',
              shortkeys: 'd',
              requireAlternativeValue: false
            }
          },
          {
            type: 'Task',
            id: '1',
            attributes: {
              colors: ['#25605e', '#31807d', '#3da09c'],
              createdAt: '2021-11-05T07:03:18Z',
              description: 'Addresses to fact check',
              name: 'Addresses',
              priority: 0,
              rounds: 3,
              taskRecordsCount: 900,
              taskRecordsDoneCount: 6,
              embeddableLinks: false,
              userTaskRecordsCount: 100,
              userTaskRecordsDoneCount: 7,
              userProgressByRound: {
                1: 0,
                2: 0.0,
                3: 7.07070707070707
              },
              userProgress: 7.000000000000001,
              status: 'OPEN',
              progress: 6.419753086419753,
              progressByRound: {
                1: 6.0,
                2: 6.60377358490566,
                3: 7.07070707070707
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
                  count: 3
                },
                data: [
                  {
                    type: 'User',
                    id: '1'
                  },
                  {
                    type: 'User',
                    id: '2'
                  },
                  {
                    type: 'User',
                    id: '3'
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
              self: 'http://localhost:9009/api/v1/tasks/1/'
            }
          },
          {
            type: 'Task',
            id: '3',
            attributes: {
              colors: ['#f3dd04', '#fcec4e', '#fdf59f'],
              createdAt: '2021-11-05T07:03:18Z',
              description: 'List of shop addresses',
              name: 'Shops',
              priority: 1,
              rounds: 3,
              taskRecordsCount: 999,
              taskRecordsDoneCount: 1,
              embeddableLinks: false,
              userTaskRecordsCount: 1,
              userTaskRecordsDoneCount: 0,
              userProgressByRound: {
                1: 0,
                2: 0,
                3: 0.0
              },
              userProgress: 0.0,
              status: 'OPEN',
              progress: 17.763157894736842,
              progressByRound: {
                1: 24.0,
                2: 5.0,
                3: 25.0
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
                  count: 4
                },
                data: [
                  {
                    type: 'User',
                    id: '1'
                  },
                  {
                    type: 'User',
                    id: '2'
                  },
                  {
                    type: 'User',
                    id: '3'
                  },
                  {
                    type: 'User',
                    id: '4'
                  }
                ]
              },
              project: {
                data: {
                  type: 'Project',
                  id: '2'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/tasks/3/'
            }
          },
          {
            type: 'User',
            id: '2',
            attributes: {
              firstName: '',
              lastName: '',
              username: 'django',
              email: '',
              emailMd5: 'd41d8cd98f00b204e9800998ecf8427e'
            },
            links: {
              self: 'http://localhost:9009/api/v1/users/2/'
            }
          },
          {
            type: 'User',
            id: '1',
            attributes: {
              firstName: '',
              lastName: '',
              username: 'olivia',
              email: '',
              emailMd5: 'd41d8cd98f00b204e9800998ecf8427e'
            },
            links: {
              self: 'http://localhost:9009/api/v1/users/3/'
            }
          }
        ]
      })
    )
  })
]
