import '@/store'
import Task from '@/models/Task'

describe('Task', () => {
  beforeAll(async () => {
    await Task.api().get()
  })

  afterAll(() => {
    Task.deleteAll()
  })

  it('should return a list of task record', () => {
    expect(Task.all()).toHaveLength(5)
  })

  it('should return a name and a description', () => {
    expect(Task.find(1).name).toBe('Addresses')
    expect(Task.find(1).description).toBe('A collection of adresses to fact check.')
  })

  it('should not return a nested choiceGroup if not requested explicitely', () => {
    expect(Task.find(1).choiceGroup).toBeNull()
  })

  it('should return a choiceGroup if requested explicitely', () => {
    const task = Task.query().with('choiceGroup').find(2)
    expect(task.choiceGroup).not.toBeNull()
    expect(task.choiceGroup.id).toBe('1')
    expect(task.choiceGroup.name).toBe('Is it correct?')
  })
})
