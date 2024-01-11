import TaskTemplateSetting from '@/models/TaskTemplateSetting'

export default class TaskTemplateSettingForText extends TaskTemplateSetting {
  static entity = 'TaskTemplateSettingForText'
  static baseEntity = 'TaskTemplateSetting'

  static fields () {
    return {
      ...super.fields(),
    }
  }
}
