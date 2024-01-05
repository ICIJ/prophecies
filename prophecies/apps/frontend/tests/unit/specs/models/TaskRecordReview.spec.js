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
    expect(TaskRecordReview.all()).toHaveLength(6)
    expect(TaskRecordReview.find(37)).not.toBeNull()
  })

  it('should return a nested of task record', () => {
    expect(TaskRecordReview.query().with('taskRecord').find(37).taskRecord.predictedValue).toBe('France')
  })

  it('should return a status', async () => {
    expect(TaskRecordReview.find(37).status).toBe('DONE')
  })

  it('should return a note', async () => {
    expect(TaskRecordReview.find(37).note).toBe('This is bad')
  })

  it('should return an alternativeValue', async () => {
    expect(TaskRecordReview.find(37).alternativeValue).toBe('FRA')
  })

  it('should return a choice', async () => {
    expect(TaskRecordReview.query().with('choice').find(37).choice.id).toBe('2')
  })
})
