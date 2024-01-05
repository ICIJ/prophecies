import { rest } from 'msw'

export default [
  rest.get('/api/v1/task-record-medias', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        links: {
          first: "http://localhost/api/v1/task-record-media/?page%5Bnumber%5D=1",
          last: "http://localhost/api/v1/task-record-media/?page%5Bnumber%5D=1",
          next: null,
          prev: null
        },
        data: [
          {
            type: "TaskRecordMedia",
            id: "0",
            attributes: {
              file: "http://localhost/media/task/4/5414ac75076a45f662a4df07e7373e434cb0bc1ae289d12dbb0341fc64e5d8da2fb7d99c1d6b99143ec3b0dbf30beea3_FzmtBWi.jpeg",
              mediaType: "IMAGE",
              mimeType: "image/jpeg",
              taskId: "3",
              taskRecordId: "40",
              uid: "5414ac75076a45f662a4df07e7373e434cb0bc1ae289d12dbb0341fc64e5d8da2fb7d99c1d6b99143ec3b0dbf30beea3"
            },
            links: {
              self: "http://localhost/api/v1/task-record-media/0/"
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
