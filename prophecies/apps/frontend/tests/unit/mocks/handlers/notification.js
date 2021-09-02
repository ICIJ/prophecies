import { rest } from 'msw'

export default [
  rest.get('/api/v1/notifications', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        links: {
          first: 'http://localhost/api/v1/notifications/?page%5Bnumber%5D=1',
          last: 'http://localhost/api/v1/notifications/?page%5Bnumber%5D=1',
          next: null,
          prev: null
        },
        data: [
          {
            type: 'Notification',
            id: '4',
            attributes: {
              read: true,
              readAt: '2021-09-02T14:03:27.635214Z'
            },
            relationships: {
              recipient: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              action: {
                data: {
                  type: 'Action',
                  id: '91'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/notifications/4/'
            }
          },
          {
            type: 'Notification',
            id: '1',
            attributes: {
              read: false,
              readAt: null
            },
            relationships: {
              recipient: {
                data: {
                  type: 'User',
                  id: '2'
                }
              },
              action: {
                data: {
                  type: 'Action',
                  id: '86'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/notifications/1/'
            }
          }
        ],
        included: [
          {
            type: 'Action',
            id: '86',
            attributes: {
              verb: 'mentioned',
              data: null,
              public: true,
              description: null,
              timestamp: '2021-09-01T19:27:39.502275Z'
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
                  type: 'Tip',
                  id: '1'
                }
              },
              target: {
                data: {
                  type: 'User',
                  id: '2'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/actions/86/'
            }
          },
          {
            type: 'Action',
            id: '91',
            attributes: {
              verb: 'mentioned',
              data: null,
              public: true,
              description: null,
              timestamp: '2021-09-01T21:14:10.562340Z'
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
                  type: 'TaskRecordReview',
                  id: '38'
                }
              },
              target: {
                data: {
                  type: 'User',
                  id: '2'
                }
              }
            },
            links: {
              self: 'http://localhost/api/v1/actions/91/'
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
            count: 2
          }
        }
      })
    )
  })
]
