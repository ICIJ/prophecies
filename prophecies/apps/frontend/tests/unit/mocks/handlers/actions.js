import { rest } from 'msw'
export default [
  rest.get('/api/v1/actions', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'Action',
            id: '353',
            attributes: {
              verb: 'created-aggregate',
              data: null,
              public: true,
              description: null,
              timestamp: '2022-02-15T00:00:00Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'ActionAggregate',
                  id: '53'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/actions/675/'
            }
          },
          {
            type: 'Action',
            id: '352',
            attributes: {
              verb: 'created-aggregate',
              data: null,
              public: true,
              description: null,
              timestamp: '2022-02-15T00:00:00Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'ActionAggregate',
                  id: '54'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/actions/675/'
            }
          },
          {
            type: 'Action',
            id: '675',
            attributes: {
              verb: 'created-aggregate',
              data: null,
              public: true,
              description: null,
              timestamp: '2022-02-15T00:00:00Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'ActionAggregate',
                  id: '55'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/actions/675/'
            }
          },
          {
            type: 'Action',
            id: '676',
            attributes: {
              verb: 'created-aggregate',
              data: null,
              public: true,
              description: null,
              timestamp: '2022-02-14T00:00:00Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'ActionAggregate',
                  id: '56'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/actions/676/'
            }
          },
          {
            type: 'Action',
            id: '677',
            attributes: {
              verb: 'created-aggregate',
              data: null,
              public: true,
              description: null,
              timestamp: '2022-02-11T00:00:00Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'ActionAggregate',
                  id: '57'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/actions/677/'
            }
          },
          {
            type: 'Action',
            id: '1200',
            attributes: {
              verb: 'created-aggregate',
              data: null,
              public: true,
              description: null,
              timestamp: '2022-02-11T00:00:00Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'ActionAggregate',
                  id: '58'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/actions/1200/'
            }
          },
          {
            type: 'Action',
            id: '911',
            attributes: {
              verb: 'mentioned',
              data: {},
              public: true,
              description: null,
              timestamp: '2021-10-14T15:40:56.323633Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '4'
                }
              },
              actionObject: {
                data: {
                  type: 'TaskRecordReview',
                  id: '1006'
                }
              },
              target: {
                data: {
                  type: 'User',
                  id: '1'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/907/'
            }
          },
          {
            type: 'Action',
            id: '910',
            attributes: {
              verb: 'reviewed',
              data: {
                task_id: 4
              },
              public: true,
              description: null,
              timestamp: '2021-10-14T15:31:27.978439Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: {
                  type: 'Choice',
                  id: '4'
                }
              },
              target: {
                data: {
                  type: 'TaskRecordReview',
                  id: '1001'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/910/'
            }
          },
          {
            type: 'Action',
            id: '909',
            attributes: {
              verb: 'reviewed',
              data: {
                task_id: 4
              },
              public: true,
              description: null,
              timestamp: '2021-10-14T15:31:18.479454Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: {
                  type: 'Choice',
                  id: '5'
                }
              },
              target: {
                data: {
                  type: 'TaskRecordReview',
                  id: '1001'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/909/'
            }
          },
          {
            type: 'Action',
            id: '908',
            attributes: {
              verb: 'reviewed',
              data: {
                task_id: 4
              },
              public: true,
              description: null,
              timestamp: '2021-10-14T15:31:16.319533Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: {
                  type: 'Choice',
                  id: '4'
                }
              },
              target: {
                data: {
                  type: 'TaskRecordReview',
                  id: '1001'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/908/'
            }
          },
          {
            type: 'Action',
            id: '907',
            attributes: {
              verb: 'mentioned',
              data: {},
              public: true,
              description: null,
              timestamp: '2021-10-14T15:27:56.323633Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: {
                  type: 'TaskRecordReview',
                  id: '1006'
                }
              },
              target: {
                data: {
                  type: 'User',
                  id: '4'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/907/'
            }
          },
          {
            type: 'Action',
            id: '906',
            attributes: {
              verb: 'closed',
              data: null,
              public: true,
              description: null,
              timestamp: '2021-10-14T16:04:13.194403Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/actions/101/'
            }
          },
          {
            type: 'Action',
            id: '905',
            attributes: {
              verb: 'reviewed',
              data: {
                task_id: 4
              },
              public: true,
              description: null,
              timestamp: '2021-10-14T15:27:34.923303Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
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
                  id: '1006'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/905/'
            }
          },
          {
            type: 'Action',
            id: '904',
            attributes: {
              verb: 'reviewed',
              data: {
                task_id: 4
              },
              public: true,
              description: null,
              timestamp: '2021-10-14T15:27:33.340242Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: {
                  type: 'Choice',
                  id: '3'
                }
              },
              target: {
                data: {
                  type: 'TaskRecordReview',
                  id: '1005'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/904/'
            }
          },
          {
            type: 'Action',
            id: '903',
            attributes: {
              verb: 'reviewed',
              data: {
                task_id: 4
              },
              public: true,
              description: null,
              timestamp: '2021-10-14T15:27:30.143090Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
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
                  id: '1004'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/903/'
            }
          },
          {
            type: 'Action',
            id: '902',
            attributes: {
              verb: 'reviewed',
              data: {
                task_id: 4
              },
              public: true,
              description: null,
              timestamp: '2021-10-14T15:27:24.555403Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
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
                  id: '1003'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/902/'
            }
          },
          {
            type: 'Action',
            id: '901',
            attributes: {
              verb: 'selected',
              data: {
                task_id: 4,
                alternative_value: 'POL'
              },
              public: true,
              description: null,
              timestamp: '2021-10-14T15:27:18.530297Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'TaskRecordReview',
                  id: '1002'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/actions/901/'
            }
          }
        ],
        included: [
          {
            type: 'ActionAggregate',
            id: '53',
            attributes: {
              verb: 'selected',
              date: '2022-02-15',
              count: 6
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
            id: '54',
            attributes: {
              verb: 'selected',
              date: '2022-02-15',
              count: 3
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
            id: '55',
            attributes: {
              verb: 'reviewed',
              date: '2022-02-15',
              count: 3
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
            id: '56',
            attributes: {
              verb: 'reviewed',
              date: '2022-02-14',
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
            id: '57',
            attributes: {
              verb: 'reviewed',
              date: '2022-02-11',
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
            id: '58',
            attributes: {
              verb: 'cancelled',
              date: '2022-02-11',
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
            id: '3',
            attributes: {
              name: "Don't know",
              value: 'unknown',
              shortkeys: 'd',
              requireAlternativeValue: false
            }
          },
          {
            type: 'Choice',
            id: '4',
            attributes: {
              name: 'Open',
              value: 'open',
              shortkeys: 'o',
              requireAlternativeValue: false
            }
          },
          {
            type: 'Choice',
            id: '5',
            attributes: {
              name: 'Closed',
              value: 'closed',
              shortkeys: 'c',
              requireAlternativeValue: false
            }
          },
          {
            type: 'TaskRecordReview',
            id: '1001',
            attributes: {
              status: 'DONE',
              note: null,
              noteCreatedAt: null,
              noteUpdatedAt: null,
              taskId: '4',
              taskRecordId: '10167',
              alternativeValue: null
            },
            relationships: {
              checker: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              choice: {
                data: {
                  type: 'Choice',
                  id: '4'
                }
              }
            },
            links: {
              self: 'http://pph.icij.org/api/v1/task-record-reviews/1001/'
            }
          },
          {
            type: 'TaskRecordReview',
            id: '1002',
            attributes: {
              status: 'DONE',
              note: null,
              noteCreatedAt: null,
              noteUpdatedAt: null,
              taskId: '4',
              taskRecordId: '10256',
              alternativeValue: 'POL'
            },
            relationships: {
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
            },
            links: {
              self: 'http://pph.icij.org/api/v1/task-record-reviews/1002/'
            }
          },
          {
            type: 'Action',
            id: '1003',
            attributes: {
              verb: 'open',
              data: null,
              public: true,
              description: null,
              timestamp: '2021-10-14T15:37:56.314810Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/actions/101/'
            }
          },
          {
            type: 'Action',
            id: '1004',
            attributes: {
              verb: 'closed',
              data: null,
              public: true,
              description: null,
              timestamp: '2021-10-14T15:34:56.314810Z'
            },
            relationships: {
              actor: {
                data: {
                  type: 'User',
                  id: '1'
                }
              },
              actionObject: {
                data: null
              },
              target: {
                data: {
                  type: 'Task',
                  id: '3'
                }
              }
            },
            links: {
              self: 'http://localhost:9009/api/v1/actions/101/'
            }
          },
          {
            type: 'TaskRecordReview',
            id: '1005',
            attributes: {
              status: 'DONE',
              note: null,
              noteCreatedAt: null,
              noteUpdatedAt: null,
              taskId: '4',
              taskRecordId: '10645',
              alternativeValue: null
            },
            relationships: {
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
            },
            links: {
              self: 'http://pph.icij.org/api/v1/task-record-reviews/1005/'
            }
          },
          {
            type: 'TaskRecordReview',
            id: '1006',
            attributes: {
              status: 'DONE',
              note: "@sledesert I'm not sure!",
              noteCreatedAt: '2021-10-14T15:27:56.314810Z',
              noteUpdatedAt: null,
              taskId: '4',
              taskRecordId: '10936',
              alternativeValue: null
            },
            relationships: {
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
            },
            links: {
              self: 'http://pph.icij.org/api/v1/task-record-reviews/1006/'
            }
          },
          {
            type: 'User',
            id: '1',
            attributes: {
              firstName: 'Pierre',
              lastName: 'Romera',
              username: 'promera',
              emailMd5: '115cd1929f14bdff9c8a53d9cea6e42b',
              isStaff: true,
              csrfToken: null
            },
            links: {
              self: 'http://pph.icij.org/api/v1/users/1/'
            }
          },
          {
            type: 'User',
            id: '4',
            attributes: {
              firstName: 'Soline',
              lastName: 'Ledésert',
              username: 'sledesert',
              emailMd5: '64fbaed6bb0e585e61369038bb3bdc3c',
              isStaff: true,
              csrfToken: null
            },
            links: {
              self: 'http://pph.icij.org/api/v1/users/4/'
            }
          },
          {
            type: 'Task',
            id: '3',
            attributes: {},
            links: {
              self: 'http://pph.icij.org/api/v1/tasks/1/'
            }
          }
        ]
      })
    )
  })
]
