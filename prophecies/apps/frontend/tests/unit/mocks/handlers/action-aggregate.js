import { rest } from 'msw'
export default [
  rest.get('/api/v1/action-aggregates', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'ActionAggregate',
            id: '1',
            attributes: {
              verb: 'selected',
              date: '2021-12-13',
              count: 1
            },
            relationships: {
              user: {
                data: {
                  type: 'User',
                  id: '4'
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
            type: 'ActionAggregate',
            id: '2',
            attributes: {
              verb: 'reviewed',
              date: '2021-12-13',
              count: 3
            },
            relationships: {
              user: {
                data: {
                  type: 'User',
                  id: '4'
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
            type: 'ActionAggregate',
            id: '3',
            attributes: {
              verb: 'reviewed',
              date: '2021-12-13',
              count: 9
            },
            relationships: {
              user: {
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
            type: 'ActionAggregate',
            id: '4',
            attributes: {
              verb: 'reviewed',
              date: '2021-12-09',
              count: 87
            },
            relationships: {
              user: {
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
            type: 'ActionAggregate',
            id: '5',
            attributes: {
              verb: 'cancelled',
              date: '2021-12-09',
              count: 34
            },
            relationships: {
              user: {
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
            type: 'ActionAggregate',
            id: '6',
            attributes: {
              verb: 'reviewed',
              date: '2021-12-20',
              count: 3
            },
            relationships: {
              user: {
                data: {
                  type: 'User',
                  id: '4'
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
            type: 'ActionAggregate',
            id: '7',
            attributes: {
              verb: 'cancelled',
              date: '2021-12-20',
              count: 3
            },
            relationships: {
              user: {
                data: {
                  type: 'User',
                  id: '4'
                }
              },
              task: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              }
            }
          }
        ]
      })
    )
  })
]
