import '@/store'
import User from '@/models/User'
import Tip from '@/models/Tip'

describe('Tip', () => {
  beforeAll(async () => {
    await Tip.api().get()
  })

  afterAll(() => {
    Tip.deleteAll()
  })

  it('should retrieve 7 tips', () => {
    expect(Tip.all()).toHaveLength(7)
  })

  it('should have one user object as creator', () => {
    const { creator } = Tip.query().with('creator').find('4')
    expect(creator.id).toBe('1')
    expect(creator.username).toBe('django')
  })

  it('should have one task object', () => {
    const { task } = Tip.query().with('task').find('4')
    expect(task.id).toBe('2')
  })

  it('should have one project object', () => {
    const { project } = Tip.query().with('project').find('4')
    expect(project.id).toBe('1')
  })

  it('should have one task object with its nested relationships', () => {
    const {
      task: { choiceGroup }
    } = Tip.query().with('task').with('task.choiceGroup').find('4')
    expect(choiceGroup.id).toBe('1')
  })

  it('should have an accessor with parsed version of the description', () => {
    const data = { id: 1000, description: 'Lorem **ipsum** dolor sit _amet_.' }
    Tip.create({ data })
    expect(Tip.find(1000).descriptionHTML).toContain('<p>Lorem <strong>ipsum</strong> dolor sit <em>amet</em>.</p>')
  })

  it('should have an accessor with parsed version of the description, including mention', () => {
    const data = { id: 1000, description: 'Hi @pirhoo, read **this**!' }
    Tip.create({ data })
    expect(Tip.find(1000).descriptionHTML).toContain(
      '<p>Hi <span class="mention">@pirhoo</span>, read <strong>this</strong>!</p>'
    )
  })

  it('should have an accessor with parsed version of the description, including mention to the current user', async () => {
    await User.api().me()
    const data = { id: 1000, description: 'Hi @django and @caroline, read **this**!' }
    Tip.create({ data })
    expect(Tip.find(1000).descriptionHTML).toContain(
      '<p>Hi <span class="mention mention--is-me">@django</span> and <span class="mention">@caroline</span>, read <strong>this</strong>!</p>'
    )
  })
})
