import '@/store'
import Tip from '@/models/Tip'

describe('Tip', () => {
  beforeAll(async () => {
    await Tip.api().get()
  })

  afterAll(() => {
    Tip.deleteAll()
  })

  it('should retrieve 2 tips', async () => {
    expect(Tip.all()).toHaveLength(2)
  })

  it('should have one user object as creator', async () => {
    const { creator } = Tip.query().with('creator').find('4')
    expect(creator.id).toBe('1')
    expect(creator.username).toBe('django')
  })

  it('should have one task object', async () => {
    const { task } = Tip.query().with('task').find('4')
    expect(task.id).toBe('2')
  })

  it('should have one project object', async () => {
    const { project } = Tip.query().with('project').find('4')
    expect(project.id).toBe('1')
  })

  it('should have one task object with its nested relationships', async () => {
    const { task: { choiceGroup } } =
    Tip.query()
      .with('task')
      .with('task.choiceGroup')
      .find('4')
    expect(choiceGroup.id).toBe('1')
  })
})
