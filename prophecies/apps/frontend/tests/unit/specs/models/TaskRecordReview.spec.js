import '@/store'
import TaskRecordReview from '@/models/TaskRecordReview'

describe('TaskRecordReview', () => {
  beforeAll(async () => {
    await TaskRecordReview.api().get()
  })

  afterAll(() => {
    TaskRecordReview.deleteAll()
  })

  it('should return a list of task record', () => {
    expect(TaskRecordReview.all()).toHaveLength(1)
    expect(TaskRecordReview.find(37).url).toBe('http://localhost/api/v1/task-record-reviews/37/')
  })

  it('should return a nested of task record', () => {
    expect(TaskRecordReview.query().with('task_record').find(37).task_record.id).toBe(1)
  })

  it('should return a choice', async () => {
    expect(TaskRecordReview.find(37).choice).toBe(2)
  })

  it('should return a status', async () => {
    expect(TaskRecordReview.find(37).status).toBe('DONE')
  })

  it('should return a note', async () => {
    expect(TaskRecordReview.find(37).note).toBe('This is bad')
  })

  it('should return an alternative_value', async () => {
    expect(TaskRecordReview.find(37).alternative_value).toBe('FRA')
  })
})
