import { rest } from 'msw'

export default [
  rest.get('/api/v1/tips', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'Tip',
            id: '8',
            attributes: {
              name: 'tip for test 8',
              description: 'test description 8',
              createdAt: '2021-09-02T12:58:16.113007Z',
              updatedAt: '2021-09-02T12:58:16.113038Z'
            },
            relationships: {
              project: {
                data: {
                  type: 'Project',
                  id: '2'
                }
              },
              creator: {
                data: {
                  type: 'User',
                  id: '1'
                }
              }
            }
          },
          {
            type: 'Tip',
            id: '7',
            attributes: {
              name: 'Tips without project',
              description: 'test description 7',
              createdAt: '2021-09-02T12:58:16.113007Z',
              updatedAt: '2021-09-02T12:58:16.113038Z'
            },
            relationships: {
              creator: {
                data: {
                  type: 'User',
                  id: '1'
                }
              }
            }
          },
          {
            type: 'Tip',
            id: '6',
            attributes: {
              name: 'tip for test 6',
              description: 'test description 6',
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
                  id: '5'
                }
              }
            }
          },
          {
            type: 'Tip',
            id: '5',
            attributes: {
              name: 'tip for test 5',
              description: 'test description 5',
              createdAt: '2021-09-02T12:58:16.113007Z',
              updatedAt: '2021-09-02T12:58:16.113038Z'
            },
            relationships: {
              project: {
                data: {
                  type: 'Project',
                  id: '2'
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
                  id: '3'
                }
              }
            }
          },
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
                  id: '3'
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
                  id: '4'
                }
              }
            }
          },
          {
            type: 'Tip',
            id: '2',
            attributes: {
              name: 'tip for test 2',
              description: 'test description 2',
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
            type: 'Project',
            id: '2',
            attributes: {
              name: 'Chronos'
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
              self: 'http://localhost/api/v1/projects/2/'
            }
          },
          {
            type: 'Project',
            id: '3',
            attributes: {
              name: 'Demeter'
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
              self: 'http://localhost/api/v1/projects/3/'
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
              status: 'OPEN',
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
            type: 'Task',
            id: '3',
            attributes: {
              colors: [
                '#5e5906',
                '#ce970d',
                '#f8c00a'
              ],
              description: 'Review Shops',
              name: 'Shops',
              priority: 1,
              rounds: 3
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
                  id: '2'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/tasks/3/'
            }
          },
          {
            type: 'Task',
            id: '4',
            attributes: {
              colors: [
                '#602541',
                '#c01764',
                '#ee0cd9'
              ],
              description: 'Review Paintings',
              name: 'Paintings',
              priority: 1,
              rounds: 3
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
                  id: '3'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/tasks/4/'
            }
          },
          {
            type: 'Task',
            id: '5',
            attributes: {
              colors: [
                '#602541',
                '#c01764',
                '#ee0cd9'
              ],
              description: 'Review Addresses',
              name: 'Addresses',
              priority: 1,
              rounds: 3
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
              self: 'http://localhost/api/v1/tasks/5/'
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
              isStaff: true
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
