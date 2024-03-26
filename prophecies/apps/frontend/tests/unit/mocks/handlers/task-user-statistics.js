import { rest } from 'msw'

export default [
  rest.get('/api/v1/task-user-statistics', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'TaskUserStatistics',
            id: '2',
            attributes: {
              round: 1,
              doneCount: 12,
              pendingCount: 187,
              totalCount: 199,
              progress: 6.030150753768844
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '1'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '1'
                }
              }
            }
          },
          {
            type: 'TaskUserStatistics',
            id: '3',
            attributes: {
              round: 2,
              doneCount: 7,
              pendingCount: 98,
              totalCount: 105,
              progress: 6.666666666666667
            },
            relationships: {
              task: {
                data: {
                  type: 'Task',
                  id: '1'
                }
              },
              checker: {
                data: {
                  type: 'User',
                  id: '2'
                }
              }
            }
          },
          {
            type: 'TaskUserStatistics',
            id: '1',
            attributes: {
              round: 1,
              doneCount: 43,
              pendingCount: 57,
              totalCount: 100,
              progress: 43.0
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
              }
            }
          },
          {
            type: 'TaskUserStatistics',
            id: '4',
            attributes: {
              round: 2,
              doneCount: 2,
              pendingCount: 95,
              totalCount: 97,
              progress: 2.0618556701030926
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
              }
            }
          },
          {
            type: 'TaskUserStatistics',
            id: '5',
            attributes: {
              round: 3,
              doneCount: 1,
              pendingCount: 2,
              totalCount: 3,
              progress: 33.33333333333333
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
              }
            }
          },
          {
            type: 'TaskUserStatistics',
            id: '6',
            attributes: {
              round: 1,
              doneCount: 5,
              pendingCount: 95,
              totalCount: 100,
              progress: 5.0
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
              }
            }
          },
          {
            type: 'TaskUserStatistics',
            id: '7',
            attributes: {
              round: 3,
              doneCount: 0,
              pendingCount: 1,
              totalCount: 1,
              progress: 0.0
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
              }
            }
          }
        ],
        included: [
          {
            type: 'Task',
            id: '1',
            attributes: {
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
            id: '1',
            attributes: {
              firstName: '',
              lastName: '',
              username: 'olivia',
              email: '',
              emailMd5: '455b74ff540a58bc42064d32e574d93b',
              isStaff: true,
              lastLogin: '2022-01-18T17:13:39.571175Z'
            },
            links: {
              self: 'http://localhost:9009/api/v1/users/1/'
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
              emailMd5: 'd41d8cd98f00b204e9800998ecf8427e',
              isStaff: true,
              lastLogin: '2022-01-28T10:21:44.271657Z'
            },
            links: {
              self: 'http://localhost:9009/api/v1/users/2/'
            }
          }
        ]
      })
    )
  })
]
