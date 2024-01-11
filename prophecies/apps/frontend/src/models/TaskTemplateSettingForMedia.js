import TaskTemplateSetting from '@/models/TaskTemplateSetting'

export default class TaskTemplateSettingForMedia extends TaskTemplateSetting {
  static entity = 'TaskTemplateSettingForMedia'
  static baseEntity = 'TaskTemplateSetting'

  static fields () {
    return {
      ...super.fields(),
    }
  }
}
