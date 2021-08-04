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
    expect(TaskRecordReview.all()).toHaveLength(3)
    expect(TaskRecordReview.find(37)).not.toBeNull()
  })

  it('should return a nested of task record', () => {
    expect(TaskRecordReview.query().with('task_record').find(37).task_record.predicted_value).toBe('France')
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

  it('should return a choice', async () => {
    expect(TaskRecordReview.query().with('choice').find(37).choice.id).toBe('2')
  })
})
